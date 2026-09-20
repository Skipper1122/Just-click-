#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HorrorObjectiveSystem.generated.h"

UENUM(BlueprintType)
enum class EObjectState : uint8 { Inactive, Active, Completed, Failed };

USTRUCT(BlueprintType)
struct FObjective
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite) FName Id;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) FText Title;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) EObjectState State = EObjectState::Inactive;
    UPROPERTY(EditAnywhere, BlueprintReadWrite) TArray<FName> Prerequisites;
};

UCLASS()
class HORRORGAME_API AHorrorObjectiveSystem : public AActor
{
    GENERATED_BODY()

public:
    AHorrorObjectiveSystem();

    UPROPERTY(Replicated, EditAnywhere, BlueprintReadOnly)
    TArray<FObjective> Objectives;

    UFUNCTION(BlueprintCallable)
    bool ServerActivate(FName Id);

    UFUNCTION(BlueprintCallable)
    bool ServerComplete(FName Id);

    UFUNCTION(BlueprintPure)
    bool IsCompleted(FName Id) const;

protected:
    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeReplicatedProps) const override;
    bool PrerequisitesMet(const FObjective& Objective) const;
};
