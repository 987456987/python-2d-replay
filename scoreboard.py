import pygame

def draw_scoreboard(screen, fontLarge, fontMed, ctColor, tColor, ctTeamList, tTeamList):
    # Draw Counter-Terrorists label
    ctTeamLabel = fontLarge.render("Counter-Terrorists", True, ctColor)
    screen.blit(ctTeamLabel, (0, 0))

    # Draw Terrorists label
    tTeamLabel = fontLarge.render("Terrorists", True, tColor)
    screen.blit(tTeamLabel, (0, 475))

    # Draw Counter-Terrorists team
    draw_team(screen, fontLarge, fontMed, ctColor, ctTeamList, 33)

    # Draw Terrorists team
    draw_team(screen, fontLarge, fontMed, tColor, tTeamList, 508)

def draw_team(screen, fontLarge, fontMed, team_color, team_list, starting_y):
    for index, player in enumerate(team_list):
        yPos = (index * 88) + starting_y

        # Background
        player_surface = pygame.Surface((400, 74), pygame.SRCALPHA)
        player_surface.fill((37, 34, 44))
        player_rect = (0, yPos)
        screen.blit(player_surface, player_rect)

        # Health
        health_surface = pygame.Surface((player["HP"] * 4, 25), pygame.SRCALPHA)
        health_surface.fill(team_color)
        health_rect = (0, yPos)
        screen.blit(health_surface, health_rect)

        health_label = fontMed.render(str(player["HP"]), True, (255, 255, 255))
        screen.blit(health_label, (0, yPos + 5))

        # PlayerName
        playerLabel = fontLarge.render(player["Name"], True, (255, 255, 255))
        screen.blit(playerLabel, (75, yPos))

        # Money
        moneyLabel = fontLarge.render("$" + str(player["Money"]), True, (255, 255, 255))
        screen.blit(moneyLabel, (325, yPos + 45))
