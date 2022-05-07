// JngMkk data to mysql
package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strconv"

	_ "github.com/go-sql-driver/mysql"
)

type disease []struct {
	DiseaseName string `json:"diseaseName"`
	EnglishName string `json:"englishName"`
	Symptom     string `json:"symptom"`
	Environment string `json:"environment"`
	Precaution  string `json:"precaution"`
}

// Json파일 파싱
func loadJson() disease {
	var disea disease
	data, err := os.Open("/home/ubuntu/finalproject/dags/data/plantdisease.json")
	if err != nil {
		log.Fatalln(err)
	}

	defer data.Close()

	val, err := ioutil.ReadAll(data)
	if err != nil {
		log.Fatalln(err)
	}

	json.Unmarshal(val, &disea)
	return disea
}

func main() {
	var diseaseId string
	diseaseJson := loadJson()

	// MYSQL 열기
	db, err := sql.Open("mysql", "root:1234@tcp(127.0.0.1:3306)/finalproject")
	if err != nil {
		log.Fatalln("a", err)
	}

	defer db.Close()

	// 테이블 있으면 삭제
	_, erro := db.Exec("DROP TABLE IF EXISTS plantdisease")
	if erro != nil {
		log.Fatalln("drop table", erro)
	}

	// 테이블 생성
	_, err2 := db.Exec(
		"CREATE TABLE plantdisease (diseaseId VARCHAR(3), diseaseName VARCHAR(30), englishName VARCHAR(30), symptom TEXT, environment TEXT, precaution TEXT, PRIMARY KEY(diseaseId)) charset = utf8;")
	if err2 != nil {
		log.Fatalln("b", err2)
	}

	// JSON 파일 table에 insert
	var err3 error
	var res sql.Result
	for i, v := range diseaseJson {
		if i < 9 {
			diseaseId = "D0" + strconv.Itoa(i+1)
			res, err3 = db.Exec(fmt.Sprintf("INSERT INTO plantdisease VALUES (%q, %q, %q, %q, %q, %q)", diseaseId, v.DiseaseName, v.EnglishName, v.Symptom, v.Environment, v.Precaution))
		} else {
			diseaseId = "D" + strconv.Itoa(i+1)
			res, err3 = db.Exec(fmt.Sprintf("INSERT INTO plantdisease VALUES (%q, %q, %q, %q, %q, %q)", diseaseId, v.DiseaseName, v.EnglishName, v.Symptom, v.Environment, v.Precaution))
		}
		if err3 != nil {
			log.Fatalln("c", err3)
		}

		_, err4 := res.LastInsertId()
		if err4 != nil {
			log.Fatalln("d", err4)
		}
	}
}
