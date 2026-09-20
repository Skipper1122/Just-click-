# Psychological Horror Co-op — C++ Foundation

Unreal Engine 5 C++ foundation for a 1–4 player psychological/co-op survival horror game.

## Scope
This repository now contains a modular gameplay foundation rather than pretending to be a finished AAA game. It covers:
- server-authoritative player health/stamina/fear state
- interaction and inventory primitives
- network-ready doors/objectives
- AI Director with stress-aware horror pacing
- monster state machine foundation
- centralized tunable configuration
- debug-friendly architecture

## Recommended engine
Unreal Engine 5.6+.

## Suggested next modules
1. Enhanced Input + first-person camera/animation
2. Online Subsystem / EOS lobby and session layer
3. MetaSounds/Audio Components + spatial voice provider
4. NavMesh + perception + full monster behavior tree
5. replicated puzzle framework
6. procedural event selection and save system
7. UMG menus/settings
8. dedicated-server packaging and automation tests

The source is intentionally modular so each subsystem can be replaced without rewriting the whole game.
