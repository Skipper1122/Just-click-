#include "HorrorInventoryComponent.h"
#include "Net/UnrealNetwork.h"

UHorrorInventoryComponent::UHorrorInventoryComponent()
{
    SetIsReplicatedByDefault(true);
}

void UHorrorInventoryComponent::BeginPlay()
{
    Super::BeginPlay();
    if (HasAuthority()) Slots.SetNum(MaxSlots);
}

bool UHorrorInventoryComponent::ServerTryAddItem(EItemType ItemType, int32 Quantity)
{
    if (!GetOwner() || !GetOwner()->HasAuthority() || Quantity <= 0) return false;

    for (FInventorySlot& Slot : Slots)
    {
        if (!Slot.IsEmpty() && Slot.ItemType == ItemType)
        {
            Slot.Quantity += Quantity;
            return true;
        }
    }

    for (FInventorySlot& Slot : Slots)
    {
        if (Slot.IsEmpty())
        {
            Slot.ItemType = ItemType;
            Slot.Quantity = Quantity;
            return true;
        }
    }
    return false;
}

bool UHorrorInventoryComponent::ServerTryRemoveItem(EItemType ItemType, int32 Quantity)
{
    if (!GetOwner() || !GetOwner()->HasAuthority() || Quantity <= 0) return false;

    for (FInventorySlot& Slot : Slots)
    {
        if (!Slot.IsEmpty() && Slot.ItemType == ItemType && Slot.Quantity >= Quantity)
        {
            Slot.Quantity -= Quantity;
            if (Slot.Quantity == 0) Slot = FInventorySlot{};
            return true;
        }
    }
    return false;
}

bool UHorrorInventoryComponent::HasItem(EItemType ItemType, int32 Quantity) const
{
    for (const FInventorySlot& Slot : Slots)
        if (Slot.ItemType == ItemType && Slot.Quantity >= Quantity) return true;
    return false;
}

void UHorrorInventoryComponent::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeReplicatedProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeReplicatedProps);
    DOREPLIFETIME(UHorrorInventoryComponent, MaxSlots);
    DOREPLIFETIME(UHorrorInventoryComponent, Slots);
}
