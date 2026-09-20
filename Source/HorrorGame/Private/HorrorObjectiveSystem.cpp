#include "HorrorObjectiveSystem.h"
#include "Net/UnrealNetwork.h"

AHorrorObjectiveSystem::AHorrorObjectiveSystem()
{
    bReplicates = true;
}

bool AHorrorObjectiveSystem::PrerequisitesMet(const FObjective& Objective) const
{
    for (const FName Required : Objective.Prerequisites)
        if (!IsCompleted(Required)) return false;
    return true;
}

bool AHorrorObjectiveSystem::ServerActivate(FName Id)
{
    if (!HasAuthority()) return false;
    for (FObjective& O : Objectives)
    {
        if (O.Id == Id && O.State == EObjectState::Inactive && PrerequisitesMet(O))
        {
            O.State = EObjectState::Active;
            return true;
        }
    }
    return false;
}

bool AHorrorObjectiveSystem::ServerComplete(FName Id)
{
    if (!HasAuthority()) return false;
    for (FObjective& O : Objectives)
    {
        if (O.Id == Id && O.State == EObjectState::Active)
        {
            O.State = EObjectState::Completed;
            return true;
        }
    }
    return false;
}

bool AHorrorObjectiveSystem::IsCompleted(FName Id) const
{
    for (const FObjective& O : Objectives)
        if (O.Id == Id) return O.State == EObjectState::Completed;
    return false;
}

void AHorrorObjectiveSystem::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeReplicatedProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeReplicatedProps);
    DOREPLIFETIME(AHorrorObjectiveSystem, Objectives);
}
