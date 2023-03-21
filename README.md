# ChanAlyzer
ChanAlyzer is a Python program that analyzes threads on the 4chan board /biz/ and generates a word cloud image based on the text in the threads.

## Installation
1. Install Python 3.x if you haven't already.
2. Clone or download the ChanAlyzer repository.
3. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage
To run ChanAlyzer, use the following command:

```bash
python chanalyzer.py [-s]
```

The -s flag is optional and indicates whether to save a new snapshot of the catalo!
g page. If the -s flag is not provided, the program will load the existing snapshot.

The program will output a word cloud image file named ChanAlyzer_< timestamp >.png in the current working directory.

## Contributing
If you encounter any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## License
This program is licensed under the MIT License. See the LICENSE file for details.
