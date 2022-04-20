package main

import (
	"github.com/JngMkk/plant/dryplant"
	"github.com/JngMkk/plant/plantinfo"
)

const k = ""

func main() {
	plantList := plantinfo.GetPlantList(k)
	plantinfo.PlantListToCsv(plantList)
	plantinfo.PlantInfoToCsv(k)
	dryplant.DryPlInfoToCsv(k)
}
