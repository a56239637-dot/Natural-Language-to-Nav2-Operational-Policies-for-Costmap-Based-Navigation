# Natural-Language to Nav2: Operational Policies for Costmap-Based Navigation

[Project page](https://a56239637-dot.github.io/Natural-Language-to-Nav2-Project-Page/)

Turn natural-language instructions into Nav2 goals and costmap constraints.
An LLM generates a policy, the bridge validates it, and Nav2 handles path
planning and motion control.

## Packages

- [policy_bridge](policy_bridge/) — LLM interface, policy validation, mission queue, and map GUI.
- [my_costmap_layers](my_costmap_layers/) — Keepout, soft-cost, and object-avoidance plugins.

## Installation

Requires **Ubuntu 22.04**, **ROS 2 Humble**, **Nav2**, and **Ollama**.

```bash
mkdir -p nav2_policy_ws/src
cd nav2_policy_ws/src
git clone https://github.com/a56239637-dot/Natural-Language-to-Nav2-Operational-Policies-for-Costmap-Based-Navigation.git
cd ..

source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
sudo apt install ros-humble-tf-transformations
python3 -m pip install torch
colcon build --symlink-install --packages-select my_costmap_layers policy_bridge
```

For camera-based person detection, also install `ultralytics`:
`python3 -m pip install ultralytics`.

## Usage

Start with a working Nav2 robot or simulation. Add the policy plugins to the
global costmap before the inflation layer, then restart Nav2.

<details>
<summary>Nav2 configuration</summary>

Merge the following into your Nav2 parameters, keeping your existing sensor-layer settings.

```yaml
global_costmap:
  global_costmap:
    ros__parameters:
      plugins:
        - static_layer
        - obstacle_layer
        - keepout_command_layer
        - zone_softcost_layer
        - object_avoidance_layer
        - inflation_layer
      keepout_command_layer:
        plugin: "my_costmap_layers::KeepoutCommandLayer"
      zone_softcost_layer:
        plugin: "my_costmap_layers::ZoneSoftCostLayer"
      object_avoidance_layer:
        plugin: "my_costmap_layers::ObjectAvoidanceLayer"
```

Soft costs use integers from 0 to 252.

</details>

Start Ollama with `ollama serve` if it is not already running. In another
terminal, download a model:

```bash
ollama pull qwen3:8b
```

From the workspace root:

```bash
source install/setup.bash
ros2 run policy_bridge policy_bridge_gui
```

In **Map / Setup**, load the map YAML and define zones and waypoints. Select an
installed model and enter a command using those labels:

```text
D is blocked for loading today, so deliver to WP5 without using that aisle.
Deliver to WP8 without getting too close to anyone working nearby.
```

## Data

- [Command benchmark](benchmarks/benchmark-data.json): 150 navigation commands,
  100 contradictory commands, reference policies, and 15 prompt demonstrations.
- [Keepout comparison](data/keepout-comparison/runs/): `odometry.csv` and
  `ground_truth.csv` from five native-filter and five custom-layer runs.
- [Rule-based baseline](policy_bridge/evaluation/README.md): parser and standalone usage.

## License

All rights reserved by the anonymous authors. Third-party licenses apply.
