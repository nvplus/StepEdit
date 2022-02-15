## StepEdit
Web-based simfile editor
### Simfile Parser
Parses an `.sm` file into JSON. To use, run `python parse-simfile.py song.sm`. It will create a new file called `result.json`.
#### Example results.json
Results are abridged for brevity.
`python parse-simfile.py 'Chocolate Groove.sm'`
```JSON
{
    "metadata": {
        "TITLE": "Chocolate Groove",
        "ARTIST": "Plexi.",
        "CREDIT": "nv",
        "MUSIC": "Chocolate Groove.ogg",
        "SAMPLESTART": "137.162",
        "SAMPLELENGTH": "25.565",
        "SELECTABLE": "YES",
        "OFFSET": "0.055",
        "BPMS": {
            "0.000": "230.000"
        },
    }
    "diffs": [
        {
            "playstyle": "dance-single",
            "description": "nv 40*/89*/16/2",
            "difficulty": "Challenge",
            "rating": "20",
            "groove_radar": ["0","0","0","0","0"],
            "steps": [["0000","0000","0000","0000"]]
        }
    ]
}
```