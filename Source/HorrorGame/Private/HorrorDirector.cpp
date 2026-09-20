#include "HorrorDirector.h"
#include "HorrorGameConfig.h"
#include "HorrorPlayerState.h"
#include "GameFramework/GameStateBase.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"

AHorrorDirector::AHorrorDirector()
{
    PrimaryActorTick.bCanEverTick = true;
    bReplicates = true;
    SetReplicateMovement(false);
}

void AHorrorDirector::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    if (!HasAuthority()) return;

    Accumulator += DeltaSeconds;
    TimeSinceLastScare += DeltaSeconds;

    if (Accumulator >= UHorrorGameConfig::Get()->DirectorUpdateInterval)
    {
        Accumulator = 0.f;
        GatherTelemetry();
    }
}

void AHorrorDirector::GatherTelemetry()
{
    TArray<APlayerState*> Players;
    if (AGameStateBase* GS = GetWorld()->GetGameState())
        Players = GS->PlayerArray;

    float StressSum = 0.f, HealthSum = 0.f;
    int32 Valid = 0;
    FVector AverageLocation = FVector::ZeroVector;

    for (APlayerState* BasePS : Players)
    {
        if (AHorrorPlayerState* PS = Cast<AHorrorPlayerState>(BasePS))
        {
            StressSum += PS->Fear;
            HealthSum += PS->Health;
            if (APawn* Pawn = PS->GetPawn())
            {
                AverageLocation += Pawn->GetActorLocation();
                ++Valid;
            }
        }
    }

    Snapshot.TeamStress = Valid ? StressSum / Valid : 0.f;
    Snapshot.AverageHealth = Valid ? HealthSum / Valid : 100.f;
    Snapshot.PlayerStress = Snapshot.TeamStress;
    Snapshot.TimeSinceLastScare = TimeSinceLastScare;

    float MaxDistance = 0.f;
    for (APlayerState* A : Players)
        for (APlayerState* B : Players)
            if (A != B && A->GetPawn() && B->GetPawn())
                MaxDistance = FMath::Max(MaxDistance,
                    FVector::Dist(A->GetPawn()->GetActorLocation(), B->GetPawn()->GetActorLocation()));

    Snapshot.DistanceBetweenPlayers = MaxDistance;
}

float AHorrorDirector::GetTensionScore() const
{
    const float Stress = Snapshot.TeamStress / 100.f;
    const float Isolation = FMath::Clamp(Snapshot.DistanceBetweenPlayers / 1800.f, 0.f, 1.f);
    const float Injury = 1.f - FMath::Clamp(Snapshot.AverageHealth / 100.f, 0.f, 1.f);
    const float Silence = FMath::Clamp(Snapshot.TimeSinceLastScare / 120.f, 0.f, 1.f);

    return FMath::Clamp(
        Stress * 0.35f +
        Isolation * 0.20f +
        Injury * 0.15f +
        Silence * 0.30f, 0.f, 1.f);
}

bool AHorrorDirector::IsCooldownActive(EHorrorEventIntensity Intensity) const
{
    if (Intensity == EHorrorEventIntensity::Major)
        return TimeSinceLastScare < UHorrorGameConfig::Get()->MinSecondsBetweenMajorScares;
    return false;
}

bool AHorrorDirector::RequestEvent(EHorrorEventIntensity MinimumIntensity, FName& OutEventId)
{
    if (!HasAuthority() || IsCooldownActive(MinimumIntensity)) return false;

    const float Tension = GetTensionScore();

    // If players are already highly stressed, deliberately prefer ambience or silence.
    if (Snapshot.TeamStress > 80.f && MinimumIntensity >= EHorrorEventIntensity::Threat)
        return false;

    if (Tension < 0.25f)
        OutEventId = TEXT("Ambient_DistantMetal");
    else if (Tension < 0.55f)
        OutEventId = TEXT("Uneasy_LightFlicker");
    else if (Tension < 0.80f)
        OutEventId = TEXT("Threat_FalseFootsteps");
    else
        OutEventId = TEXT("Major_ImpostorVoice");

    TimeSinceLastScare = 0.f;
    return true;
}
