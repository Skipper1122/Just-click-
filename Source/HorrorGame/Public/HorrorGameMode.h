#pragma once

#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "HorrorGameMode.generated.h"

UCLASS()
class HORRORGAME_API AHorrorGameMode : public AGameModeBase
{
    GENERATED_BODY()

public:
    AHorrorGameMode();

    virtual void PostLogin(APlayerController* NewPlayer) override;
    virtual void Logout(AController* Exiting) override;

protected:
    UPROPERTY(EditDefaultsOnly, Category="Game")
    int32 MaxPlayers = 4;

    UPROPERTY(EditDefaultsOnly, Category="Game")
    TSubclassOf<class AHorrorDirector> DirectorClass;
};
