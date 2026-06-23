import json
import bs4 
from experiment import Experiment
from xml_adapter import XMLConfig

def main() -> None:
    with open("/Users/avishkarborkar/Desktop/Loadmaster/Code-Quality-Software-Fundamentals/Design-Patterns/adapter/config.xml", encoding="utf8") as file:
        config = file.read()
    bs = bs4.BeautifulSoup(config, "xml")

    #Here we can't simple pass 'bs' to Experiment as it expects a Config interface
    #So we create an Adaptor, for the 'soup' object to conform to Config interface
    
    adapter = XMLConfig(bs)
    config = adapter
    experiment = Experiment(config)
    experiment.run()


if __name__ == "__main__":
    main()