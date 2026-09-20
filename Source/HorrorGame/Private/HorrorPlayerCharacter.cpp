#include "HorrorPlayerCharacter.h"
#include "HorrorPlayerState.h"
#include "HorrorGameConfig.h"
#include "Camera/CameraComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "Components/CapsuleComponent.h"

AHorrorPlayerCharacter::AHorrorPlayerCharacter()
{
    PrimaryActorTick.bCanEverTick = true;
    bReplicates = true;

    FirstPersonCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FirstPersonCamera"));
    FirstPersonCamera->SetupAttachment(GetCapsuleComponent());
    FirstPersonCamera->SetRelativeLocation(FVector(0,0,64));
    FirstPersonCamera->bUsePawnControlRotation = true;

    GetCharacterMovement()->MaxWalkSpeed = WalkSpeed;
    GetCharacterMovement()->MaxWalkSpeedCrouched = CrouchSpeed;
    GetCharacterMovement()->GetNavAgentPropertiesRef().bCanCrouch = true;
}

void AHorrorPlayerCharacter::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    if (IsLocallyControlled())
    {
        // The server owns the authoritative stamina value; input is requested by RPC.
        // Presentation-only camera/audio effects belong in the local controller.
    }
    UpdateMovement(DeltaSeconds);
}

void AHorrorPlayerCharacter::SetupPlayerInputComponent(UInputComponent* Input)
{
    Super::SetupPlayerInputComponent(Input);
    Input->BindAxis(TEXT("MoveForward"), this, &AHorrorPlayerCharacter::MoveForward);
    Input->BindAxis(TEXT("MoveRight"), this, &AHorrorPlayerCharacter::MoveRight);
    Input->BindAxis(TEXT("LookUp"), this, &AHorrorPlayerCharacter::LookUp);
    Input->BindAxis(TEXT("Turn"), this, &AHorrorPlayerCharacter::Turn);
    Input->BindAction(TEXT("Sprint"), IE_Pressed, this, &AHorrorPlayerCharacter::ServerSetSprint, true);
    Input->BindAction(TEXT("Sprint"), IE_Released, this, &AHorrorPlayerCharacter::ServerSetSprint, false);
    Input->BindAction(TEXT("Crouch"), IE_Pressed, this, &AHorrorPlayerCharacter::ServerSetCrouch, true);
    Input->BindAction(TEXT("Crouch"), IE_Released, this, &AHorrorPlayerCharacter::ServerSetCrouch, false);
}

void AHorrorPlayerCharacter::MoveForward(float Value)
{
    if (Value != 0.f) AddMovementInput(GetActorForwardVector(), Value);
}

void AHorrorPlayerCharacter::MoveRight(float Value)
{
    if (Value != 0.f) AddMovementInput(GetActorRightVector(), Value);
}

void AHorrorPlayerCharacter::LookUp(float Value) { AddControllerPitchInput(Value); }
void AHorrorPlayerCharacter::Turn(float Value) { AddControllerYawInput(Value); }

void AHorrorPlayerCharacter::ServerSetSprint_Implementation(bool bWantsSprint)
{
    AHorrorPlayerState* PS = GetPlayerState<AHorrorPlayerState>();
    if (!PS) return;
    PS->ServerSetSprinting(bWantsSprint);
    bSprintInput = bWantsSprint;
}

void AHorrorPlayerCharacter::ServerSetCrouch_Implementation(bool bWantsCrouch)
{
    AHorrorPlayerState* PS = GetPlayerState<AHorrorPlayerState>();
    if (!PS) return;
    PS->ServerSetCrouched(bWantsCrouch);
    bCrouchInput = bWantsCrouch;
    if (bWantsCrouch) Crouch(); else UnCrouch();
}

void AHorrorPlayerCharacter::ServerInteract_Implementation()
{
    // Intentionally left as the integration point for UInteractionComponent.
}

void AHorrorPlayerCharacter::UpdateMovement(float DeltaSeconds)
{
    const AHorrorPlayerState* PS = GetPlayerState<AHorrorPlayerState>();
    if (!PS) return;

    float TargetSpeed = WalkSpeed;
    if (PS->bCrouched) TargetSpeed = CrouchSpeed;
    else if (PS->bSprinting && PS->Stamina > 0.f) TargetSpeed = SprintSpeed;

    GetCharacterMovement()->MaxWalkSpeed = TargetSpeed;
}
