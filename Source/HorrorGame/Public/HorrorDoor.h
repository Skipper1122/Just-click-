#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "InteractionInterface.h"
#include "HorrorDoor.generated.h"

UCLASS()
class HORRORGAME_API AHorrorDoor : public AActor, public IInteractable
{
    GENERATED_BODY()

public:
    AHorrorDoor();

    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeReplicatedProps) const override;

    UPROPERTY(ReplicatedUsing=OnRep_Open, BlueprintReadOnly, Category="Door")
    bool bOpen = false;

    UPROPERTY(Replicated, EditAnywhere, BlueprintReadOnly, Category="Door")
    bool bLocked = false;

    UFUNCTION(BlueprintCallable)
    void ServerSetOpen(bool bNewOpen);

    virtual bool CanInteract_Implementation(AActor* Interactor) const override;
    virtual void Interact_Implementation(AActor* Interactor) override;

protected:
    UFUNCTION()
    void OnRep_Open();

    UPROPERTY(VisibleAnywhere)
    TObjectPtr<USceneComponent> Root;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
    TObjectPtr<UStaticMeshComponent> DoorMesh;

    FRotator ClosedRotation;
    FRotator OpenRotation;
};
