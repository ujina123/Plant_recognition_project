package main

import (
	"github.com/JngMkk/plant/getlist"
	"github.com/JngMkk/plant/plantinfo"
)

const k = ""

func main() {
	plantList := getlist.GetPlantList(k)
	getlist.PlantListToCsv(plantList)
	plantinfo.PlantInfoToCsv(k)
}
