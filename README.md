# yitter - yet another Twitter front-end

A project that's heavily inspired by [nitter](https://github.com/zedeus/nitter).

## Installation

### Debian based systems
```
sudo -i
apt install --no-install-recommends git redis python3-{httpx,redis,bottle,waitress}
useradd -ms /bin/bash yitter
su - yitter
git clone https://codeberg.org/PrivacyDev/yitter
cp yitter/config.py{.example,}
chmod 600 yitter/config.py
exit
cp /home/yitter/yitter/yitter.service /etc/systemd/system/
chown root:root /etc/systemd/system/yitter.service
```
Adjust the following files as needed:
- /home/yitter/yitter/config.py

```
systemctl daemon-reload
systemctl enable --now yitter
systemctl reload nginx
exit
```

## Update

```
sudo -i
su - yitter
cd yitter
git pull
exit
systemctl restart yitter
exit
```

## Instances

### Clearnet
|Instance                                                 | Cloudflare | Notes             |
|---------------------------------------------------------|------------|-------------------|
|[yitter.privacydev.net](https://yitter.privacydev.net)   | No         | official instance |

### Tor
|Instance                                                                                                                                                | Notes             |
|--------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
|[yitter.g4c3eya4clenolymqbpgwz3q3tawoxw56yhzk4vugqrl6dtu3ejvhjid.onion](http://yitter.g4c3eya4clenolymqbpgwz3q3tawoxw56yhzk4vugqrl6dtu3ejvhjid.onion)   | official instance |

## Mirrors
[Codeberg](https://codeberg.org/PrivacyDev/yitter), [GitHub](https://github.com/PrivacyDevel/yitter)

## Donations
[Monero (XMR)](https://www.getmonero.org/): `8ABDaQZQEqD1DFV6EBhUs9dBbM1FvsMBpP81JL8oRUZEetFX46MmtuHe7iV6wbC64mGwQDdrr7MKoXXuLCjRmSTnKMrBZMT` \
[Bitcoin (BTC)](https://bitcoin.org/): `bc1qql3ac9wtnnwt20r69dk9tdsh8u6vupsjdwj76w`

