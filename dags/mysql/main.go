// JngMkk data to mysql
package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"

	_ "github.com/go-sql-driver/mysql"
)

type plants []struct {
	URL          string `json:"URL"`
	Name         string `json:"name"`
	BotanyNm     string `json:"botanyNm"`
	Info         string `json:"info"`
	WaterCycle   string `json:"waterCycle"`
	WaterInfo    string `json:"waterInfo"`
	WaterExp     string `json:"waterExp"`
	WaterExpInfo string `json:"waterExpInfo"`
	Light        string `json:"light"`
	LightInfo    string `json:"lightInfo"`
	LightExp     string `json:"lightExp"`
	LightExpInfo string `json:"lightExpInfo"`
	Humidity     string `json:"humidity"`
	HumidInfo    string `json:"humidInfo"`
	HumidExp     string `json:"humidExp"`
	HumidExpInfo string `json:"humidExpInfo"`
	TempExp      string `json:"tempExp"`
	TempExpInfo  string `json:"tempExpInfo"`
}

// Json파일 파싱
func loadJson() plants {
	var plant plants
	data, err := os.Open("/home/ubuntu/finalproject/dags/data/plants.json")
	if err != nil {
		log.Fatalln(err)
	}

	defer data.Close()

	val, err := ioutil.ReadAll(data)
	if err != nil {
		log.Fatalln(err)
	}

	json.Unmarshal(val, &plant)
	return plant
}

func main() {
	plants := loadJson()

	// MYSQL 열기
	db, err := sql.Open("mysql", "root:1234@tcp(127.0.0.1:3306)/finalproject")
	if err != nil {
		log.Fatalln("a", err)
	}

	defer db.Close()

	// 테이블 있으면 삭제
	_, erro := db.Exec("DROP TABLE IF EXISTS plants")
	if erro != nil {
		log.Fatalln("drop table", erro)
	}

	// 테이블 생성
	_, err2 := db.Exec(
		"CREATE TABLE plants (plantID INT NOT NULL AUTO_INCREMENT PRIMARY KEY, URL VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, botanyNm VARCHAR(255) NOT NULL, info TEXT NOT NULL, waterCycle VARCHAR(255) NOT NULL, waterInfo VARCHAR(255) NOT NULL, waterExp VARCHAR(255) NOT NULL, waterExpInfo TEXT NOT NULL, light VARCHAR(255) NOT NULL, lightInfo VARCHAR(255) NOT NULL, lightExp VARCHAR(255) NOT NULL, lightExpInfo TEXT NOT NULL, humidity VARCHAR(255) NOT NULL, humidInfo VARCHAR(255) NOT NULL, humidExp VARCHAR(255) NOT NULL, humidExpInfo TEXT NOT NULL, tempExp VARCHAR(255) NOT NULL, tempExpInfo TEXT NOT NULL) charset = utf8;")
	if err2 != nil {
		log.Fatalln("b", err2)
	}

	// JSON 파일 table에 insert
	var err3 error
	var res sql.Result
	for _, v := range plants {
		res, err3 = db.Exec(fmt.Sprintf("INSERT INTO plants(URL, name, botanyNm, info, waterCycle, waterInfo, waterExp, waterExpInfo, light, lightInfo, lightExp, lightExpInfo, humidity, humidInfo, humidExp, humidExpInfo, tempExp, tempExpInfo) VALUES (%q, %q, %q, %q, %q, %q, %q, %q, %q, %q, %q, %q, %q, %q, %q, %q, %q, %q)", v.URL, v.Name, v.BotanyNm, v.Info, v.WaterCycle, v.WaterInfo, v.WaterExp, v.WaterExpInfo, v.Light, v.LightInfo, v.LightExp, v.LightExpInfo, v.Humidity, v.HumidInfo, v.HumidExp, v.HumidExpInfo, v.TempExp, v.TempExpInfo))

		if err3 != nil {
			log.Fatalln("c", err3)
		}

		_, err4 := res.LastInsertId()
		if err4 != nil {
			log.Fatalln("d", err4)
		}
	}
}
