"""Verify optional single-Nginx stream port remapping is backward compatible."""
import json
import os
import subprocess
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MUX_ENV={
    "NGINX_PROXY_HTTP_CONTAINER_PORT":"10080",
    "NGINX_PROXY_HTTPS_CONTAINER_PORT":"10443",
    "NGINX_PROXY_ENABLE_PROXY_PROTOCOL":"true",
    "NGINX_PROXY_TRUST_DOWNSTREAM_PROXY":"false",
}
KEYS=tuple(MUX_ENV)
def config(overrides):
    env=os.environ.copy()
    for key in KEYS:env.pop(key,None)
    env.update(overrides)
    p=subprocess.run(
        ["docker","compose","config","--format","json"],
        cwd=ROOT,env=env,check=True,text=True,capture_output=True,timeout=30,
    )
    return json.loads(p.stdout)

class StreamComposeTest(unittest.TestCase):
    def test_default_no_mux_does_not_change_the_public_80_443_ports(self):
        data=config({})
        nginx=data["services"]["nginx-proxy"]
        self.assertEqual({(p["published"],p["target"]) for p in nginx["ports"]},
                         {("80",80),("443",443)})
        self.assertIn("nginx-proxy-acme",data["services"])

    def test_optional_mux_maps_public_to_private_stream_listeners(self):
        data=config(MUX_ENV)
        nginx=data["services"]["nginx-proxy"]
        self.assertEqual({(p["published"],p["target"]) for p in nginx["ports"]},
                         {("80",10080),("443",10443)})
        self.assertEqual(len(nginx["ports"]),2)
        # PROXY header, mount, image pins are deliberately host-specific
        # and supplied by the Ansible docker-compose.override.yml.
        self.assertFalse(any(v["target"]=="/etc/nginx/toplevel.conf.d"
                             for v in nginx["volumes"]))

if __name__=="__main__":
    unittest.main()
