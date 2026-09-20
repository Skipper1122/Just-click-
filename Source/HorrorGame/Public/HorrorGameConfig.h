#pragma once

#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "HorrorGameConfig.generated.h"

UCLASS(BlueprintType, Config=Game, DefaultConfig)
class HORRORGAME_API UHorrorGameConfig : public UObject
{
    GENERATED_BODY()

public:
    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category="Player|Stamina")
    float MaxStamina = 100.f;

    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category="Player|Stamina")
    float SprintDrainPerSecond = 15.f;

    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category="Player|Stamina")
    float StaminaRecoveryPerSecond = 20.f;

    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category="Player|Health")
    float MaxHealth = 100.f;

    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category="Player|Revive")
    float ReviveDuration = 6.f;

    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category="Horror")
    float MinSecondsBetweenMajorScares = 45.f;

    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category="Horror")
    float DirectorUpdateInterval = 1.f;

    UPROPERTY(Config, EditAnywhere, BlueprintReadOnly, Category="Network")
    float RemoteStateSendInterval = 0.05f;

    UFUNCTION(BlueprintPure, Category="Config")
    static const UHorrorGameConfig* Get()
    {
        return GetDefault<UHorrorGameConfig>();
    }
};
