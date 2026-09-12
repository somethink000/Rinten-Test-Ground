{
  "Emitters": [
    {
      "Name": "Rock",
      "Identifier": "2095fa70-e08d-5135-aa46-efcfbf77c694",
      "Enabled": true,
      "MaxParticles": 4,
      "Places": 0,
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1",
      "Anchor": null,
      "Delay": 0,
      "Duration": 0,
      "PreWarm": 0,
      "TimeScale": 1,
      "Timing": "GameTime",
      "SpawnModules": [
        {
          "__type": "Rinten.SpawnBurstModule",
          "Stage": "Spawn",
          "Count": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "29f7cff7-94a1-55b7-a1e1-2ce2e0fce9f4",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": null,
          "Sample": "Random",
          "Along": {
            "UseParameter": false,
            "Value": 0,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "AlignToShape": false,
          "Shape": "Box",
          "Offset": "-7,9,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "3,0.5,3",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "914fabe2-a36c-5ac5-a610-1b7b89677d6c",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeVelocityModule",
          "Stage": "Initialize",
          "Velocity": {
            "UseParameter": false,
            "Value": {
              "X": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "6.5,7.5,0,0"
              },
              "Y": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-6.5,-7.5,0,0"
              },
              "Z": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-0.5,0.5,0,0"
              }
            },
            "ParameterName": null,
            "Multiplier": 1,
            "ScaleParameterName": "Speed",
            "SlotName": null,
            "SlotMode": "Replace",
            "IsBound": false
          },
          "Scatter": {
            "UseParameter": false,
            "Value": 0,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "LocalSpace": false,
          "InheritEmitterVelocity": false,
          "InheritScale": 1,
          "Drift": {
            "X": 0,
            "Y": 0,
            "Z": 0
          },
          "Identifier": "351a90c8-9640-564c-8a4c-a4f6e792a2f3",
          "Name": "Velocity",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 4,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "81129df7-665a-5d06-87cc-316ebbaa2701",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": {
              "Type": "Range",
              "Evaluation": "Seed",
              "Constants": "0.600000024,1,0,0"
            },
            "ParameterName": "Size",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "InheritEmitterScale": true,
          "Identifier": "db8af838-a30f-58fe-aabb-01aaf1cab4a3",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": {
              "Type": "Gradient",
              "Evaluation": "Life",
              "GradientA": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "1,0.6902,0.4392,1"
                  },
                  {
                    "t": 1,
                    "c": "1,0.3765,0.1255,1"
                  }
                ],
                "alpha": null
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "1,0.6902,0.4392,1"
                  },
                  {
                    "t": 1,
                    "c": "1,0.3765,0.1255,1"
                  }
                ],
                "alpha": null
              }
            },
            "ParameterName": null,
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 1.3,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "c741087d-1b6c-5e91-8d3d-7ce8c0307da7",
          "Name": "Color",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeRotationModule",
          "Stage": "Initialize",
          "Rotation": {
            "X": {
              "Type": "Range",
              "Evaluation": "Seed",
              "Constants": "0,360,0,0"
            },
            "Y": {
              "Type": "Range",
              "Evaluation": "Seed",
              "Constants": "0,360,0,0"
            },
            "Z": {
              "Type": "Range",
              "Evaluation": "Seed",
              "Constants": "0,360,0,0"
            }
          },
          "Identifier": "a773ad77-43d2-5d27-b8fa-a37582c1dca1",
          "Name": "Rotation",
          "Enabled": true
        },
        {
          "__type": "Rinten.ParticleCollisionModule",
          "Stage": "Initialize",
          "Ignore": "",
          "Radius": {
            "UseParameter": false,
            "Value": 0.15,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "DieOnHitChance": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Prefabs": [],
          "PrefabChance": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "PrefabRotation": {
            "UseParameter": false,
            "Value": 0,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "PrefabAlign": false,
          "Bounce": {
            "UseParameter": false,
            "Value": 0,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Friction": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Bumpiness": {
            "UseParameter": false,
            "Value": 0,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "PushStrength": {
            "UseParameter": false,
            "Value": 0,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "a23b5f1d-15d8-5980-bbec-92bf9a3fb335",
          "Name": "Collision",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.SpinModule",
          "Stage": "Update",
          "Speed": {
            "UseParameter": false,
            "Value": {
              "X": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-300,300,0,0"
              },
              "Y": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-300,300,0,0"
              },
              "Z": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-300,300,0,0"
              }
            },
            "ParameterName": null,
            "Multiplier": 1,
            "ScaleParameterName": null,
            "SlotName": null,
            "SlotMode": "Replace",
            "IsBound": false
          },
          "Identifier": "661c132a-da68-555b-bf11-b6b9ee5d387b",
          "Name": "Spin",
          "Enabled": true
        },
        {
          "__type": "Rinten.GravityModule",
          "Stage": "Update",
          "Force": {
            "UseParameter": false,
            "Value": {
              "X": 0,
              "Y": -4,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1,
            "ScaleParameterName": null,
            "SlotName": null,
            "SlotMode": "Replace",
            "IsBound": false
          },
          "Identifier": "cfb8ffc8-3e8a-53de-9fe6-522ece546bda",
          "Name": "Gravity",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.ModelRenderModule",
          "Stage": "Render",
          "Models": [
            {
              "Model": "models/dev/sphere.mdl",
              "MaterialGroup": null,
              "BodyGroups": 18446744073709551615
            }
          ],
          "Scale": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "RotateWithObject": false,
          "CastShadows": true,
          "Identifier": "f7221f17-3cec-58b7-9ec6-8bcb76b98bd3",
          "Name": "Model",
          "Enabled": true
        },
        {
          "__type": "Rinten.TrailRenderModule",
          "Stage": "Render",
          "Material": null,
          "Width": {
            "UseParameter": true,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": {
                "rangey": "0,0.200000003",
                "frames": [
                  {
                    "x": 0,
                    "y": 1,
                    "in": 0,
                    "out": 0,
                    "mode": "Linear"
                  },
                  {
                    "x": 1,
                    "y": 0,
                    "in": 0,
                    "out": 0,
                    "mode": "Linear"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,0.349999994",
                "frames": [
                  {
                    "x": 0,
                    "y": 1,
                    "in": 0,
                    "out": 0,
                    "mode": "Linear"
                  },
                  {
                    "x": 1,
                    "y": 0,
                    "in": 0,
                    "out": 0,
                    "mode": "Linear"
                  }
                ]
              }
            },
            "ParameterName": "Trail",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 0.6,
            "IsBound": true
          },
          "Color": {
            "UseParameter": false,
            "Value": {
              "Type": "Gradient",
              "Evaluation": "Life",
              "GradientA": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "1,0.8157,0.5647,0.8"
                  },
                  {
                    "t": 0.5,
                    "c": "1,0.3765,0.1255,0.5"
                  },
                  {
                    "t": 1,
                    "c": "0.251,0.0627,0,0"
                  }
                ],
                "alpha": null
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "1,0.8157,0.5647,0.8"
                  },
                  {
                    "t": 0.5,
                    "c": "1,0.3765,0.1255,0.5"
                  },
                  {
                    "t": 1,
                    "c": "0.251,0.0627,0,0"
                  }
                ],
                "alpha": null
              }
            },
            "ParameterName": null,
            "IsBound": false
          },
          "UnitsPerTexture": 0.5,
          "Scroll": 0,
          "MaxPoints": 48,
          "PointDistance": 0.1,
          "LifeTime": 0.7,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": false,
          "TintFromParticle": true,
          "Identifier": "5ecb53ca-3625-5f7d-a048-14a6ff3ad147",
          "Name": "Trail",
          "Enabled": true
        },
        {
          "__type": "Rinten.SpawnEffectOnDeathModule",
          "Stage": "Render",
          "Effect": "fx/impact.fx",
          "Chance": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Scale": {
            "UseParameter": true,
            "Value": 1,
            "ParameterName": "Impact",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "AlignToVelocity": false,
          "OnCollision": true,
          "OnExpiry": false,
          "MaxAlive": 3,
          "Identifier": "d84dcc91-d7b2-555c-baaa-b312285dc3e1",
          "Name": "Effect On Death",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "1,0.5647,0.251,1",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": true,
            "Value": 8,
            "ParameterName": "Glow",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Radius": {
            "UseParameter": false,
            "Value": 5,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Attenuation": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "MaxLights": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Ratio": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "UseParticleColor": false,
          "CastShadows": false,
          "Identifier": "6ff9e815-cf26-5a9d-aa1e-1a65d96432a3",
          "Name": "Light",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 3.5,
  "Looping": true,
  "Shapes": [],
  "Slots": [],
  "Anchors": [],
  "FloatParameters": [
    {
      "DefaultValue": 1,
      "Min": 0.5,
      "Max": 2,
      "Name": "Speed",
      "Identifier": "c5652ff3-2ee3-566a-8605-b1bee9390b2f"
    },
    {
      "DefaultValue": 1,
      "Min": 0.2,
      "Max": 3,
      "Name": "Size",
      "Identifier": "aa28643f-24dc-5d1d-8f12-1fa1d19f187c"
    },
    {
      "DefaultValue": 1,
      "Min": 0,
      "Max": 3,
      "Name": "Trail",
      "Identifier": "7ea32034-b747-50f8-9a8a-ed735911693a"
    },
    {
      "DefaultValue": 1,
      "Min": 0.3,
      "Max": 3,
      "Name": "Impact",
      "Identifier": "12472d1f-d6d4-5fff-8a61-e0751eedc2e4"
    },
    {
      "DefaultValue": 1,
      "Min": 0,
      "Max": 3,
      "Name": "Glow",
      "Identifier": "6e941755-ba13-5f6b-b668-a3913c5a96a2"
    }
  ],
  "VectorParameters": [],
  "ColorParameters": [
    {
      "DefaultValue": {
        "Type": "Gradient",
        "Evaluation": "Life",
        "GradientA": {
          "blend": "Linear",
          "color": [
            {
              "t": 0,
              "c": "1,0.9412,0.7529,1"
            },
            {
              "t": 0.4,
              "c": "1,0.5647,0.1882,1"
            },
            {
              "t": 1,
              "c": "0.502,0.1255,0,1"
            }
          ],
          "alpha": null
        },
        "GradientB": {
          "blend": "Linear",
          "color": [
            {
              "t": 0,
              "c": "1,0.9412,0.7529,1"
            },
            {
              "t": 0.4,
              "c": "1,0.5647,0.1882,1"
            },
            {
              "t": 1,
              "c": "0.502,0.1255,0,1"
            }
          ],
          "alpha": null
        }
      },
      "Name": "Fire",
      "Identifier": "5f190a93-e58c-5820-a68c-b386637989b7"
    }
  ],
  "__references": [],
  "__version": 0
}