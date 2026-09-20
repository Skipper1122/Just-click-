#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "HorrorInventoryComponent.generated.h"

UENUM(BlueprintType)
enum class EItemType : uint8
{
    Flashlight, Battery, Key, Fuse, Medkit, Bandage, Radio, Camera, ResearchNote, Special
};

USTRUCT(BlueprintType)
struct FInventorySlot
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    EItemType ItemType = EItemType::Special;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    int32 Quantity = 0;

    bool IsEmpty() const { return Quantity <= 0; }
};

UCLASS(ClassGroup=(Horror), meta=(BlueprintSpawnableComponent))
class HORRORGAME_API UHorrorInventoryComponent : public UActorComponent
{
    GENERATED_BODY()

public:
    UHorrorInventoryComponent();

    UPROPERTY(Replicated, EditAnywhere, BlueprintReadOnly, Category="Inventory")
    int32 MaxSlots = 6;

    UPROPERTY(Replicated, BlueprintReadOnly, Category="Inventory")
    TArray<FInventorySlot> Slots;

    UFUNCTION(BlueprintCallable)
    bool ServerTryAddItem(EItemType ItemType, int32 Quantity = 1);

    UFUNCTION(BlueprintCallable)
    bool ServerTryRemoveItem(EItemType ItemType, int32 Quantity = 1);

    UFUNCTION(BlueprintPure)
    bool HasItem(EItemType ItemType, int32 Quantity = 1) const;

protected:
    virtual void BeginPlay() override;
    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;
};
