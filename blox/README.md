# Blox (B4ox)

In `docker-compose.yml` file change the volume to mount the `blox` directory to `/app` directory in the container.
```
    volumes:
      - ./blox:/app

```

```
bin/up -d
bin/enter-root
pytest -vv
```
