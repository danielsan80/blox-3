# Triblox (3lox)

In `docker-compose.yml` file change the volume to mount the `triblox` directory to `/app` directory in the container.
```
    volumes:
      - ./triblox:/app

```

```
bin/up -d
bin/enter-root
pytest -vv
```


https://www.plantuml.com/plantuml/uml/JOynpi8m38Ntdi8N-2-GuLSbEaCNOEbYKWj5f4sLk1K8UdUYoi7DP3_xVSwh4sFaUV3LXFQ1Tm96J_2kAW3hCIKuX13xB41-KqW6sk16tjgkMoYoivJLYrGow5qaoowC1ffIvj6gt0qZtAU1mdoLKbT_RDd6_Hzk-yPginQttXVxWduc0-VsqvokHv1JalFlln1Kq6YgQQXihcdivy5_0G00

``` plantuml
@startuml
package coord {

  class Coord {
    pos: Point
    \\vertices: Vertices
    \\direction: Direction
  }

  class Point {
    x: int
    y: int
  }

  class Vertices {
    a: Point
    b: Point
    c: Point
  }
  class Direction {
    value: UP|DOWN 
  }

  Coord -> Point
  Coord -> Vertices
  Coord -> Direction
}

@enduml
```


https://chatgpt.com/share/680bc503-8d7c-8013-9b80-810206829d42
