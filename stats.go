package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"time"

	dem "github.com/markus-wa/demoinfocs-golang/v4/pkg/demoinfocs"
	"github.com/markus-wa/demoinfocs-golang/v4/pkg/demoinfocs/events"
	"github.com/markus-wa/demoinfocs-golang/v4/pkg/demoinfocs/msgs2"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage: go run script.go <path_to_demo_file>")
		return
	}

	// Get the demo file path from the command-line argument
	demoPath := os.Args[1]

	// Open the demo file
	f, err := os.Open(demoPath)
	if err != nil {
		fmt.Println("Failed to open the demo file:", err)
		return
	}

	// Extract the filename from the path
	demoFileName := filepath.Base(demoPath)

	// Remove the extension from the filename
	demoFileName = strings.TrimSuffix(demoFileName, filepath.Ext(demoFileName))

	// Open and parse the demo file.
	parser := dem.NewParser(f)
	defer parser.Close()

	mapName := ""

	parser.RegisterNetMessageHandler(func(msg *msgs2.CSVCMsg_ServerInfo) {
		mapName = msg.GetMapName()
	})

	matchStarted := false

	// Parse the demo and track player positions.
	startTime := time.Now()
	fmt.Println("Demo Parsing Started...")

	bombState := 0
	roundWinner := 0
	var teamScore [2]int

	parser.RegisterEventHandler(func(e events.RoundStart) {
		matchStarted = true
	})

	parser.RegisterEventHandler(func(e events.RoundEnd) {
		roundWinner = int(e.Winner)
	})

	fmt.Println("Parsing Completed Saving Data...")
	// Store the data in a JSON file.
	jsonData, err := json.MarshalIndent(demoData, "", "  ")
	if err != nil {
		fmt.Println("Error marshaling JSON:", err)
		return
	}

	jsonFileName := "_internal/data/" + demoFileName + ".json"
	jsonFile, err := os.Create(jsonFileName)
	if err != nil {
		fmt.Println("Error creating JSON file:", err)
		return
	}
	defer jsonFile.Close()

	_, err = jsonFile.Write(jsonData)
	if err != nil {
		fmt.Println("Error writing JSON data to file:", err)
		return
	}

}
