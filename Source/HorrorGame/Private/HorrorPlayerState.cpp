#include "HorrorPlayerState.h"
#include "HorrorGameConfig.h"
#include "Net/UnrealNetwork.h"

AHorrorPlayerState::AHorrorPlayerState()
{
    bReplicates = true;
    Health = UHorrorGameConfig::Get()->MaxHealth;
    Stamina = UHorrorGameConfig::Get()->MaxStamina;
}

void AHorrorPlayerState::ServerApplyDamage(float Amount)
{
    if (!HasAuthority() || Amount <= 0.f || LifeState == EHorrorLifeState::Dead) return;

    Health = FMath::Clamp(Health - Amount, 0.f, UHorrorGameConfig::Get()->MaxHealth);
    if (Health <= 0.f && LifeState == EHorrorLifeState::Alive)
        LifeState = EHorrorLifeState::Downed;
}

void AHorrorPlayerState::ServerAddFear(float Amount)
{
    if (!HasAuthority()) return;
    Fear = FMath::Clamp(Fear + Amount, 0.f, 100.f);
}

void AHorrorPlayerState::ServerSetSprinting(bool bNewSprinting)
{
    if (!HasAuthority() || !IsAlive()) return;
    bSprinting = bNewSprinting;
}

void AHorrorPlayerState::ServerSetCrouched(bool bNewCrouched)
{
    if (!HasAuthority() || !IsAlive()) return;
    bCrouched = bNewCrouched;
}

void AHorrorPlayerState::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeReplicatedProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeReplicatedProps);
    DOREPLIFETIME(AHorrorPlayerState, Health);
    DOREPLIFETIME(AHorrorPlayerState, Stamina);
    DOREPLIFETIME(AHorrorPlayerState, Fear);
    DOREPLIFETIME(AHorrorPlayerState, LifeState);
    DOREPLIFETIME(AHorrorPlayerState, bSprinting);
    DOREPLIFETIME(AHorrorPlayerState, bCrouched);
}
