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

type Grenades struct {
	FragGrenade       bool
	SmokeGrenade      bool
	Decoy             bool
	IncendiaryGrenade bool
	Molotov           bool
	Flashbang         int
}

// PlayerPosition represents the position of a player at a given tick.
type PlayerPosition struct {
	Name           string
	Position       Vector
	Rotation       float32
	IsAlive        bool
	Team           int
	IsFiring       bool
	Weapon         string
	Bomb           bool
	FlashDuration  float32
	FlashRemaining float32
	FlashBy        int
	HP             int
	Money          int
	DefuseKit      bool
	Armor          bool
	Helmet         bool
	Utility        Grenades
	Primary        string
	Seconday       string
	Kills          int
	Deaths         int
	Assists        int
}

// MatchInfo represents data from outside of a individual player
type MatchInfo struct {
	BombPosition Vector
	BombOnGround bool
	BombState    int //0 = Not Planted, 1 = Planted, 2 = Defused, 3 = Exploded
}

// RoundData represents the tick data for a round.
type TickData struct {
	PlayerPositions []PlayerPosition
	MatchInfo       MatchInfo
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

	bombState := 0

	parser.RegisterEventHandler(func(e events.RoundEndOfficial) {
		// Event handler to track the start of each round.
		roundNumber++

		bombState = 0

		// Add the last round data.
		roundDataList = append(roundDataList, currentRoundData)

		// Initialize a new round data.
		currentRoundData = RoundData{
			RoundNumber: roundNumber,
		}
	})

	firingStatus := make(map[string]bool)

	parser.RegisterEventHandler(func(e events.WeaponFire) {
		firingStatus[e.Shooter.Name] = true
	})

	flashedBy := make(map[string]int)
	parser.RegisterEventHandler(func(e events.PlayerFlashed) {
		flashedBy[e.Player.Name] = int(e.Attacker.GetTeam())
	})

	// BOMB EVENTS
	parser.RegisterEventHandler(func(e events.BombPlanted) {
		bombState = 1
	})
	parser.RegisterEventHandler(func(e events.BombDefused) {
		bombState = 2
	})
	parser.RegisterEventHandler(func(e events.BombExplode) {
		bombState = 3
	})
	////////////////

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
			flashbangs := 0
			smoke := false
			decoy := false
			molotov := false
			incendiary := false
			frag := false
			secondary := ""
			primary := ""
			for _, q := range p.Weapons() {
				if q.String() == "Flashbang" {
					flashbangs = q.AmmoInMagazine() + q.AmmoReserve()
				} else if q.String() == "Smoke Grenade" {
					smoke = true
				} else if q.String() == "HE Grenade" {
					frag = true
				} else if q.String() == "Incendiary Grenade" {
					incendiary = true
				} else if q.String() == "Molotov" {
					molotov = true
				} else if q.String() == "Decoy" {
					decoy = true
				} else if q.Class() == 1 {
					secondary = q.String()
				} else if q.Class() == 2 || q.Class() == 3 || q.Class() == 4 {
					primary = q.String()
				}
			}

			currentUtil := Grenades{
				FragGrenade:       frag,
				SmokeGrenade:      smoke,
				Decoy:             decoy,
				IncendiaryGrenade: incendiary,
				Molotov:           molotov,
				Flashbang:         flashbangs,
			}

			value, exists := firingStatus[p.Name]
			playerFire := false
			if exists {
				playerFire = value
				firingStatus[p.Name] = false
			}

			value1, exists1 := flashedBy[p.Name]
			flashedTeam := 0
			if exists1 {
				flashedTeam = value1
			}

			carryBomb := false
			if parser.GameState().Bomb().Carrier != nil && parser.GameState().Bomb().Carrier.Name == p.Name {
				carryBomb = true
			}

			currentWeapon := ""
			if p.ActiveWeapon() != nil {
				currentWeapon = p.ActiveWeapon().String()
			}

			currentFlashDuration := 0.00
			currentFlashRemaining := 0.00
			if p.FlashDurationTime() != 0 {
				currentFlashDuration = p.FlashDurationTime().Seconds()
				currentFlashRemaining = p.FlashDurationTimeRemaining().Seconds()
			}

			hasArmor := false
			if p.Armor() > 0 {
				hasArmor = true
			}
			playerPos := PlayerPosition{
				Name:           p.Name,
				Position:       Vector{X: p.Position().X, Y: p.Position().Y, Z: p.Position().Z},
				Rotation:       p.ViewDirectionX(),
				IsAlive:        p.IsAlive(),
				Team:           int(p.GetTeam()),
				IsFiring:       playerFire,
				Weapon:         currentWeapon,
				Bomb:           carryBomb,
				FlashDuration:  float32(currentFlashDuration),
				FlashRemaining: float32(currentFlashRemaining),
				FlashBy:        flashedTeam,
				HP:             p.Health(),
				Money:          p.Money(),
				Armor:          hasArmor,
				Helmet:         p.HasHelmet(),
				DefuseKit:      p.HasDefuseKit(),
				Utility:        currentUtil,
				Primary:        primary,
				Seconday:       secondary,
				Kills:          p.Kills(),
				Deaths:         p.Deaths(),
				Assists:        p.Assists(),
			}
			currentTickData.PlayerPositions = append(currentTickData.PlayerPositions, playerPos)
		}
		bombVector := Vector{
			X: gameState.Bomb().LastOnGroundPosition.X,
			Y: gameState.Bomb().LastOnGroundPosition.Y,
			Z: gameState.Bomb().LastOnGroundPosition.Z,
		}
		isBombOnGround := false
		if gameState.Bomb().Carrier == nil {
			isBombOnGround = true
		}
		currentMatchInfo := MatchInfo{
			BombPosition: bombVector,
			BombOnGround: isBombOnGround,
			BombState:    bombState,
		}
		currentTickData.MatchInfo = currentMatchInfo
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
