#include "MonsterAI.h"
#include "HorrorPlayerState.h"
#include "Net/UnrealNetwork.h"
#include "Kismet/GameplayStatics.h"
#include "GameFramework/CharacterMovementComponent.h"

AMonsterAI::AMonsterAI()
{
    PrimaryActorTick.bCanEverTick = true;
    bReplicates = true;
}

void AMonsterAI::Tick(float DeltaSeconds)
{
    Super::Tick(DeltaSeconds);
    StateTime += DeltaSeconds;
    if (HasAuthority()) UpdateServerAI(DeltaSeconds);
}

void AMonsterAI::UpdateServerAI(float DeltaSeconds)
{
    APawn* VisibleTarget = FindBestVisibleTarget();

    switch (State)
    {
    case EMonsterState::Idle:
        if (VisibleTarget) { TargetPawn = VisibleTarget; TransitionTo(EMonsterState::Observe); }
        break;

    case EMonsterState::Observe:
        if (!TargetPawn) { TransitionTo(EMonsterState::Search); break; }
        if (FVector::Dist(GetActorLocation(), TargetPawn->GetActorLocation()) < AttackRange)
            TransitionTo(EMonsterState::Attack);
        else if (StateTime > 3.0f)
            TransitionTo(EMonsterState::Stalk);
        break;

    case EMonsterState::Stalk:
        if (!TargetPawn) { TransitionTo(EMonsterState::Search); break; }
        if (FVector::Dist(GetActorLocation(), TargetPawn->GetActorLocation()) < 700.f)
            TransitionTo(EMonsterState::Chase);
        break;

    case EMonsterState::Chase:
        if (!TargetPawn) { TransitionTo(EMonsterState::Search); break; }
        if (FVector::Dist(GetActorLocation(), TargetPawn->GetActorLocation()) <= AttackRange)
            TransitionTo(EMonsterState::Attack);
        else
            GetCharacterMovement()->MaxWalkSpeed = 500.f;
        break;

    case EMonsterState::Attack:
        if (TargetPawn && FVector::Dist(GetActorLocation(), TargetPawn->GetActorLocation()) <= AttackRange)
        {
            if (AHorrorPlayerState* PS = TargetPawn->GetPlayerState<AHorrorPlayerState>())
                PS->ServerApplyDamage(25.f);
        }
        TransitionTo(EMonsterState::Retreat);
        break;

    case EMonsterState::Search:
        if (VisibleTarget) { TargetPawn = VisibleTarget; TransitionTo(EMonsterState::Observe); }
        else if (StateTime > 8.f) TransitionTo(EMonsterState::Idle);
        break;

    default:
        if (StateTime > 4.f) TransitionTo(EMonsterState::Search);
        break;
    }
}

APawn* AMonsterAI::FindBestVisibleTarget() const
{
    TArray<AActor*> Pawns;
    UGameplayStatics::GetAllActorsOfClass(GetWorld(), APawn::StaticClass(), Pawns);

    APawn* Best = nullptr;
    float BestScore = TNumericLimits<float>::Max();

    for (AActor* A : Pawns)
    {
        APawn* P = Cast<APawn>(A);
        if (!P || P == this) continue;
        const float D = FVector::DistSquared(GetActorLocation(), P->GetActorLocation());
        if (D > FMath::Square(SightRange)) continue;

        if (AHorrorPlayerState* PS = P->GetPlayerState<AHorrorPlayerState>())
        {
            if (!PS->IsAlive()) continue;
            if (D < BestScore) { BestScore = D; Best = P; }
        }
    }
    return Best;
}

void AMonsterAI::TransitionTo(EMonsterState NewState)
{
    if (State == NewState) return;
    State = NewState;
    StateTime = 0.f;
    OnRep_MonsterState();
}

void AMonsterAI::ServerSetState_Implementation(EMonsterState NewState)
{
    if (HasAuthority()) TransitionTo(NewState);
}

void AMonsterAI::ReportNoise(FVector NoiseLocation, float Loudness)
{
    if (!HasAuthority()) return;
    const float D = FVector::Dist(GetActorLocation(), NoiseLocation);
    if (D <= HearingRange * FMath::Clamp(Loudness, 0.1f, 2.f))
    {
        LastKnownLocation = NoiseLocation;
        LastNoiseTime = GetWorld()->GetTimeSeconds();
        if (State == EMonsterState::Idle || State == EMonsterState::Search)
            TransitionTo(EMonsterState::Investigate);
    }
}

void AMonsterAI::OnRep_MonsterState() {}

void AMonsterAI::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeReplicatedProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeReplicatedProps);
    DOREPLIFETIME(AMonsterAI, State);
    DOREPLIFETIME(AMonsterAI, TargetPawn);
}
