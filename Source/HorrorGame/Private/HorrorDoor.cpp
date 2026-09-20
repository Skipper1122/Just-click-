#include "HorrorDoor.h"
#include "Net/UnrealNetwork.h"
#include "Components/StaticMeshComponent.h"

AHorrorDoor::AHorrorDoor()
{
    bReplicates = true;
    Root = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
    SetRootComponent(Root);

    DoorMesh = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("DoorMesh"));
    DoorMesh->SetupAttachment(Root);
    DoorMesh->SetIsReplicated(false);

    ClosedRotation = FRotator::ZeroRotator;
    OpenRotation = FRotator(0.f, 90.f, 0.f);
}

bool AHorrorDoor::CanInteract_Implementation(AActor* Interactor) const
{
    return !bLocked;
}

void AHorrorDoor::Interact_Implementation(AActor* Interactor)
{
    if (HasAuthority() && !bLocked) ServerSetOpen(!bOpen);
}

void AHorrorDoor::ServerSetOpen(bool bNewOpen)
{
    if (!HasAuthority() || bLocked) return;
    bOpen = bNewOpen;
    OnRep_Open();
}

void AHorrorDoor::OnRep_Open()
{
    DoorMesh->SetRelativeRotation(bOpen ? OpenRotation : ClosedRotation);
}

void AHorrorDoor::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeReplicatedProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeReplicatedProps);
    DOREPLIFETIME(AHorrorDoor, bOpen);
    DOREPLIFETIME(AHorrorDoor, bLocked);
}
