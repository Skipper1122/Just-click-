#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HorrorDirector.generated.h"

UENUM(BlueprintType)
enum class EHorrorEventIntensity : uint8 { Ambient, Uneasy, Threat, Major };

USTRUCT(BlueprintType)
struct FHorrorDirectorSnapshot
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly) float PlayerStress = 0.f;
    UPROPERTY(BlueprintReadOnly) float TeamStress = 0.f;
    UPROPERTY(BlueprintReadOnly) float AverageHealth = 100.f;
    UPROPERTY(BlueprintReadOnly) float DistanceBetweenPlayers = 0.f;
    UPROPERTY(BlueprintReadOnly) float TimeSinceLastScare = 999.f;
    UPROPERTY(BlueprintReadOnly) float MissionProgress = 0.f;
    UPROPERTY(BlueprintReadOnly) float MonsterAwareness = 0.f;
    UPROPERTY(BlueprintReadOnly) float DarknessLevel = 0.f;
    UPROPERTY(BlueprintReadOnly) float NoiseLevel = 0.f;
};

UCLASS()
class HORRORGAME_API AHorrorDirector : public AActor
{
    GENERATED_BODY()

public:
    AHorrorDirector();

    virtual void Tick(float DeltaSeconds) override;

    UPROPERTY(BlueprintReadOnly, Category="Director")
    FHorrorDirectorSnapshot Snapshot;

    UFUNCTION(BlueprintCallable)
    bool RequestEvent(EHorrorEventIntensity MinimumIntensity, FName& OutEventId);

    UFUNCTION(BlueprintCallable)
    float GetTensionScore() const;

protected:
    float TimeSinceLastScare = 999.f;
    float Accumulator = 0.f;

    void GatherTelemetry();
    bool IsCooldownActive(EHorrorEventIntensity Intensity) const;
};
