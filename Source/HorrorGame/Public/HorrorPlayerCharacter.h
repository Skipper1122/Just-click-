#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "HorrorPlayerCharacter.generated.h"

UCLASS()
class HORRORGAME_API AHorrorPlayerCharacter : public ACharacter
{
    GENERATED_BODY()

public:
    AHorrorPlayerCharacter();

    virtual void Tick(float DeltaSeconds) override;
    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override;

    UFUNCTION(Server, Reliable)
    void ServerSetSprint(bool bWantsSprint);

    UFUNCTION(Server, Reliable)
    void ServerSetCrouch(bool bWantsCrouch);

    UFUNCTION(Server, Reliable)
    void ServerInteract();

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Movement")
    float WalkSpeed = 250.f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Movement")
    float SprintSpeed = 450.f;

    UPROPERTY(EditDefaultsOnly, BlueprintReadOnly, Category="Movement")
    float CrouchSpeed = 140.f;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Camera")
    TObjectPtr<class UCameraComponent> FirstPersonCamera;

private:
    bool bSprintInput = false;
    bool bCrouchInput = false;

    void MoveForward(float Value);
    void MoveRight(float Value);
    void LookUp(float Value);
    void Turn(float Value);
    void UpdateMovement(float DeltaSeconds);
};
