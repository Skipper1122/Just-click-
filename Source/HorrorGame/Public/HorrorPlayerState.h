#pragma once

#include "CoreMinimal.h"
#include "GameFramework/PlayerState.h"
#include "HorrorPlayerState.generated.h"

UENUM(BlueprintType)
enum class EHorrorLifeState : uint8
{
    Alive,
    Downed,
    Dead,
    Spectating
};

UCLASS()
class HORRORGAME_API AHorrorPlayerState : public APlayerState
{
    GENERATED_BODY()

public:
    AHorrorPlayerState();

    UPROPERTY(Replicated, BlueprintReadOnly, Category="Horror|State")
    float Health = 100.f;

    UPROPERTY(Replicated, BlueprintReadOnly, Category="Horror|State")
    float Stamina = 100.f;

    UPROPERTY(Replicated, BlueprintReadOnly, Category="Horror|State")
    float Fear = 0.f;

    UPROPERTY(Replicated, BlueprintReadOnly, Category="Horror|State")
    EHorrorLifeState LifeState = EHorrorLifeState::Alive;

    UPROPERTY(Replicated, BlueprintReadOnly, Category="Horror|State")
    bool bSprinting = false;

    UPROPERTY(Replicated, BlueprintReadOnly, Category="Horror|State")
    bool bCrouched = false;

    UFUNCTION(BlueprintCallable)
    void ServerApplyDamage(float Amount);

    UFUNCTION(BlueprintCallable)
    void ServerAddFear(float Amount);

    UFUNCTION(BlueprintCallable)
    void ServerSetSprinting(bool bNewSprinting);

    UFUNCTION(BlueprintCallable)
    void ServerSetCrouched(bool bNewCrouched);

    UFUNCTION(BlueprintPure)
    bool IsAlive() const { return LifeState == EHorrorLifeState::Alive; }

protected:
    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;
};
