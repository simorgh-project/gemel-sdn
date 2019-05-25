#!/usr/bin/env bash

# 1.Enable ip forward on the gateway host
sudo sysctl -w net.ipv4.ip_forward=1

# 2.Change the default policy of the iptables FORWARD chain to accept all packets on the gateway host
sudo iptables -A FORWARD -j ACCEPT

# 3.Enable masquerading on the gateway host
sudo iptables -t nat -A POSTROUTING -o ens4 -j MASQUERADE

echo \
"-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEAyzHbnh78m37sXPfw0RpExi1KQPpZCCemu/rG+UlFjCw0bs68xDJX
uwYPx+sFHfUG+xPX3mQCpstjxZ3OyuPxOOTI4QSB2o86+JNRKOtoZ0Et0SuG1IgpKlgOH7
AAzmbA7W9yKT6aELaiocoVcQq7tBYc+PtM9pLSXDoi1kckH4xbR2MYdp7vy947jw2NH4tP
X5gGpDX8NS+UXx6CcN14RrkuZRpuAO0nTu5FlI0uPMxTbcHkefuZ0gepIHOrDNaifrqdVz
LvAujLnh6gOze4IWvt2Ja2ozN4TkZtFoamm0B6bYcHFNI18O2oqs5A5+Z25K3X/4WEoKJU
eSQliv146QAAA9DayiFk2sohZAAAAAdzc2gtcnNhAAABAQDLMdueHvybfuxc9/DRGkTGLU
pA+lkIJ6a7+sb5SUWMLDRuzrzEMle7Bg/H6wUd9Qb7E9feZAKmy2PFnc7K4/E45MjhBIHa
jzr4k1Eo62hnQS3RK4bUiCkqWA4fsADOZsDtb3IpPpoQtqKhyhVxCru0Fhz4+0z2ktJcOi
LWRyQfjFtHYxh2nu/L3juPDY0fi09fmAakNfw1L5RfHoJw3XhGuS5lGm4A7SdO7kWUjS48
zFNtweR5+5nSB6kgc6sM1qJ+up1XMu8C6MueHqA7N7gha+3YlrajM3hORm0WhqabQHpthw
cU0jXw7aiqzkDn5nbkrdf/hYSgolR5JCWK/XjpAAAAAwEAAQAAAQAQTvQdgMctg8Zcv9mo
Lr+OWFw5Ut6KdQRA2iPWJjdaxMGAkz87T/8Sl630kbxbZyskQ7dztfswf+qGFeBfEGRv+I
zW4pG5hP1qrgg5jItYnjabLy8nJ7aGG4Mmr+2go0agx+0VulyLMt1ituF5rS7biVrR8PmA
YNBZbqEVKaiQj4KAf17U1vEgACVijrxNsZUGpBMBWcoCXuFHnKiy1znV3vvf7Bwwxjou/0
AK/UbHTYW6/lHhXKLQiFqh6TFni95iURcP9otK7ByeyeILl4Yv9uGJGwCNH2wk0SHbw3jE
9At68W+YQ71SvwzO0gxvWlyEXhZDPhV3PVq6R/l9YmwxAAAAgQCtkNyjWfFiWhXdK4mvIR
JUW/wIl6gO++6ft7tUc3y2ysE7Z3JASGLNv0D6cmZ56X/V4oEQdQjFt911rvOHtBbdxm3p
1KIVzLA4DM0gdD2JzD+vzf9WuwOAluVlMd+IBYGz33rXn1bf2MhJ5vEJ+rBxFuy3I9kfwU
B3qMjUlfNOjAAAAIEA/ixEpm3pR2g7uAVA932nuRqmu40MhqTXpp4+EeRCYZv8ZgabOW0F
AQ4ezaB8qwiqa+F7lbCBC35xRR517+/Ah1uxAnYYC6TEe8tMD12J5E18n/a/uGpOL91hjM
x2Vh0fUwv9XCB+4H9JZ+Tp2lHaRf5OdAt4fhxjyvHj7cC6eGsAAACBAMynx3UjfRsa9WDy
6zRF6OfT+flBwewdPwbwrEBLMrV4Rrk80YxVfhntzu5nDeVK5R1yxP/1Wmz62vUgXoTDR0
PpoiocNWaCL6AVeY7Y7i3LH1D/Z46qlpJoEkzgGEUuRbtid3B39Z3v9/xZtSFoW25I8nAn
O+h40NajWPP59jj7AAAAFGJsYWNrdnZpbmVAQmx1ZVNraWVzAQIDBAUG
-----END OPENSSH PRIVATE KEY-----" >> ~/.ssh/gw
