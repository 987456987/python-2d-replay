import pygame

from weapontable import weapon_icon_table

def draw_scoreboard(screen, fontLarge, fontMed, fontLargeWeapons, fontMedWeapons, ctColor, tColor, ctTeamList, tTeamList, Score):
    # Draw Counter-Terrorists label
    ctTeamLabel = fontLarge.render("Counter-Terrorists", True, ctColor)
    screen.blit(ctTeamLabel, (25, 10))
    
    ctTeamScoreLabel = fontLarge.render(str(Score[1]), True, ctColor)
    screen.blit(ctTeamScoreLabel, (375, 10))

    # Draw Terrorists label
    tTeamLabel = fontLarge.render("Terrorists", True, tColor)
    screen.blit(tTeamLabel, (25, 485))
    
    tTeamScoreLabel = fontLarge.render(str(Score[0]), True, tColor)
    screen.blit(tTeamScoreLabel, (375, 485))

    # Draw Counter-Terrorists team
    draw_team(screen, fontLarge, fontMed, fontLargeWeapons, fontMedWeapons, ctColor, ctTeamList, 33)

    # Draw Terrorists team
    draw_team(screen, fontLarge, fontMed, fontLargeWeapons, fontMedWeapons, tColor, tTeamList, 508)

def draw_team(screen, fontLarge, fontMed, fontLargeWeapons, fontMedWeapons, team_color, team_list, starting_y):
    for index, player in enumerate(team_list):
        yPos = (index * 88) + starting_y

        # Background
        player_surface = pygame.Surface((400, 74), pygame.SRCALPHA)
        player_surface.fill((37, 34, 44))
        player_rect = (0, yPos)
        screen.blit(player_surface, player_rect)

        # Health
        health_surface = pygame.Surface((player["HP"] * 4, 37), pygame.SRCALPHA)
        health_surface.fill(team_color)
        health_rect = (0, yPos)
        screen.blit(health_surface, health_rect)

        health_label = fontMed.render(str(player["HP"]), True, (255, 255, 255))
        screen.blit(health_label, (14, yPos + 8))

        # PlayerName
        playerLabel = fontLarge.render(player["Name"], True, (255, 255, 255))
        screen.blit(playerLabel, (95, yPos + 6))

        # Money
        moneyLabel = fontMed.render("$" + str(player["Money"]), True, (8, 217, 92))
        screen.blit(moneyLabel, (10, yPos + 46))
        if player["IsAlive"]:
            # Defuse Kit
            if player["DefuseKit"]:
                kitLabel = fontLargeWeapons.render(weapon_icon_table.get("Kit", "Unknown"), True, (255, 255, 255))
                screen.blit(kitLabel, (275, yPos + 4))
            
            # Armour
            if player["Armor"]:
                kitLabel = fontLargeWeapons.render(weapon_icon_table.get("Vest", "Unknown"), True, (255, 255, 255))
                if player["Helmet"]:
                    kitLabel = fontLargeWeapons.render(weapon_icon_table.get("Helmet", "Unknown"), True, (255, 255, 255))
                screen.blit(kitLabel, (310, yPos + 42))
                
            # Primary
            primaryLabel = fontLargeWeapons.render(weapon_icon_table.get(player["Primary"], "Unknown"), True, (255, 255, 255))
            screen.blit(primaryLabel, (315, yPos + 6))

            # Seconday
            secondayLabel = fontLargeWeapons.render(weapon_icon_table.get(player["Seconday"], "Unknown"), True, (255, 255, 255))
            screen.blit(secondayLabel, (350, yPos + 40))
            
            #Bomb
            if player["Bomb"]:
                bombLabel = fontLargeWeapons.render(weapon_icon_table.get("C4", "Unknown"), True, (255, 255, 255))
                screen.blit(bombLabel, (275, yPos + 4))
                
            #Utility
            utilityString = ""
            if player["Utility"]["Molotov"]:
                utilityString += weapon_icon_table.get("Molotov", "Unknown") + " "
            if player["Utility"]["IncendiaryGrenade"]:
                utilityString += weapon_icon_table.get("Incendiary Grenade", "Unknown") + " "
            if player["Utility"]["SmokeGrenade"]:
                utilityString += weapon_icon_table.get("Smoke Grenade", "Unknown") + " "
            if player["Utility"]["Flashbang"] > 0:
                for x in range(player["Utility"]["Flashbang"]):
                    utilityString += weapon_icon_table.get("Flashbang", "Unknown") + " "
            if player["Utility"]["Decoy"]:
                utilityString += weapon_icon_table.get("Decoy", "Unknown") + " "
            if player["Utility"]["FragGrenade"]:
                utilityString += weapon_icon_table.get("HE Grenade", "Unknown") + " "
            
            utilityLabel = fontMedWeapons.render(utilityString, True, (255, 255, 255))
            screen.blit(utilityLabel, (205, yPos + 44))
            
        #Stats
        statsLabel = fontMed.render(str(player["Kills"]) + " / " + str(player["Assists"]) + " / " + str(player["Deaths"]), True, (255, 255, 255))
        screen.blit(statsLabel, (95, yPos + 46))