#include "HorrorGameMode.h"
#include "HorrorPlayerState.h"
#include "HorrorPlayerCharacter.h"
#include "HorrorDirector.h"
#include "GameFramework/GameSession.h"

AHorrorGameMode::AHorrorGameMode()
{
    PlayerStateClass = AHorrorPlayerState::StaticClass();
    DefaultPawnClass = AHorrorPlayerCharacter::StaticClass();
    MaxPlayers = 4;
    DirectorClass = AHorrorDirector::StaticClass();
}

void AHorrorGameMode::PostLogin(APlayerController* NewPlayer)
{
    Super::PostLogin(NewPlayer);

    if (GetNumPlayers() > MaxPlayers)
    {
        NewPlayer->Destroy();
        return;
    }

    if (HasAuthority() && GetWorld()->GetAuthGameMode() == this)
    {
        if (!GetWorld()->GetTimerManager().IsTimerActive(
            FTimerHandle{}))
        {
            // Director placement should be handled by a dedicated GameState in production.
        }
    }
}

void AHorrorGameMode::Logout(AController* Exiting)
{
    Super::Logout(Exiting);
    // Player departure is intentionally non-fatal. Persistent mission state belongs to GameState.
}
