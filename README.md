# Very Small Soccer Size Simulator


## Requerimientos
    
* Blender 2.75


## Compilacion

1. Abrir vsss.blend en Blender 2.75 (en otras versiones no funciona bien)
2. File > Export > Save as Game Engine Runtime
3. Escoger una carpeta (de preferencia vacia) donde guardar el ejecutable


## Configuracion (no es necesario)

1. En $HOME_DIR crear una carpeta ".vsss_simulator"
2. Dentro de ".vsss_simulator" crear un archivo "config.json" que contenga la configuracion deseada
3. Un ejemplo de este archivo se encuentra en el repositorio con el nombre "config.jason.example"

## Comunication

* Server sends:

{
    "see": {
        "red_team": [
            [<x>, <y>, <theta>],
            [<x>, <y>, <theta>]
        ],
        "blue_team": [
            [<x>, <y>, <theta>],
            [<x>, <y>, <theta>]
        ],
        "ball": [<x>, <y>]
    }
}

* Server receive:

{
    "add_listener": {}

{
    "rm_listener": {}
}

{
    "move": {
        "red":[
            [<lin_vel>, <ang_vel>],
            [<lin_vel>, <ang_vel>]
        ]
    }
}

