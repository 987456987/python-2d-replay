package main

import (
	"encoding/json"
	"fmt"
	"os"
	"time"

	dem "github.com/markus-wa/demoinfocs-golang/v4/pkg/demoinfocs"
	"github.com/markus-wa/demoinfocs-golang/v4/pkg/demoinfocs/events"
)

// Vector represents a 3D vector.
type Vector struct {
	X, Y, Z float64
}

// PlayerPosition represents the position of a player at a given tick.
type PlayerPosition struct {
	Name     string
	Position Vector
	Rotation float32
	IsAlive  bool
	Team     int
}

// RoundData represents the tick data for a round.
type TickData struct {
	PlayerPositions []PlayerPosition
}

// RoundData represents the data for a round.
type RoundData struct {
	RoundNumber int
	Tick        []TickData
}

func main() {
	// Specify the path to the CS:GO demo file.
	demoPath := "./test.dem"

	f, err := os.Open("./" + demoPath)
	if err != nil {
		fmt.Println("Failed to open the demo file")
		return
	}

	// Open and parse the demo file.
	parser := dem.NewParser(f)
	defer parser.Close()

	// Initialize a slice to store round data.
	var roundDataList []RoundData
	var currentRoundData RoundData
	var roundNumber int

	// Parse the demo and track player positions.
	startTime := time.Now()

	parser.RegisterEventHandler(func(e events.RoundStart) {
		// Event handler to track the start of each round.
		roundNumber++

		// Add the last round data.
		roundDataList = append(roundDataList, currentRoundData)

		// Initialize a new round data.
		currentRoundData = RoundData{
			RoundNumber: roundNumber,
		}
	})

	for {
		moreFrames, err := parser.ParseNextFrame()
		if err != nil {
			// Handle the error
			fmt.Println("Error parsing frame:", err)
			break
		}
		if !moreFrames {
			// No more frames to parse, break the loop
			break
		}

		gameState := parser.GameState()

		var currentTickData TickData

		for _, p := range gameState.Participants().Playing() {
			// Store the player's position.
			playerPos := PlayerPosition{
				Name:     p.Name,
				Position: Vector{X: p.Position().X, Y: p.Position().Y, Z: p.Position().Z},
				Rotation: p.ViewDirectionX(),
				IsAlive:  p.IsAlive(),
				Team:     int(p.GetTeam()),
			}
			currentTickData.PlayerPositions = append(currentTickData.PlayerPositions, playerPos)
		}
		currentRoundData.Tick = append(currentRoundData.Tick, currentTickData)
	}

	elapsed := time.Since(startTime)

	// Store the data in a JSON file.
	jsonData, err := json.MarshalIndent(roundDataList, "", "  ")
	if err != nil {
		fmt.Println("Error marshaling JSON:", err)
		return
	}

	// Write the JSON data to a file.
	jsonFileName := "round_data.json"
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

	fmt.Printf("Data has been stored in %s\n", jsonFileName)
	fmt.Printf("Demo parsing completed in %v seconds.\n", elapsed.Seconds())
}
