#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "MonsterAI.generated.h"

UENUM(BlueprintType)
enum class EMonsterState : uint8
{
    Idle,
    Investigate,
    Observe,
    Stalk,
    Search,
    Chase,
    Attack,
    Retreat
};

UCLASS()
class HORRORGAME_API AMonsterAI : public ACharacter
{
    GENERATED_BODY()

public:
    AMonsterAI();

    virtual void Tick(float DeltaSeconds) override;

    UPROPERTY(ReplicatedUsing=OnRep_MonsterState, BlueprintReadOnly)
    EMonsterState State = EMonsterState::Idle;

    UPROPERTY(Replicated, BlueprintReadOnly)
    TObjectPtr<APawn> TargetPawn;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="AI")
    float HearingRange = 2200.f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="AI")
    float SightRange = 3500.f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="AI")
    float AttackRange = 160.f;

    UFUNCTION(Server, Reliable)
    void ServerSetState(EMonsterState NewState);

    UFUNCTION(BlueprintCallable)
    void ReportNoise(FVector NoiseLocation, float Loudness);

protected:
    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeReplicatedProps) const override;

    UFUNCTION()
    void OnRep_MonsterState();

    void UpdateServerAI(float DeltaSeconds);
    APawn* FindBestVisibleTarget() const;
    void TransitionTo(EMonsterState NewState);

    FVector LastKnownLocation = FVector::ZeroVector;
    float LastNoiseTime = -999.f;
    float StateTime = 0.f;
};
