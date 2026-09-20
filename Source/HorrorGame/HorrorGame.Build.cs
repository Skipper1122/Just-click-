using UnrealBuildTool;

public class HorrorGame : ModuleRules
{
    public HorrorGame(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core", "CoreUObject", "Engine", "NetCore", "EnhancedInput",
            "AIModule", "GameplayTasks", "NavigationSystem", "UMG"
        });

        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "Slate", "SlateCore"
        });
    }
}
