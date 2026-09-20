{
  "Emitters": [
    {
      "Name": "Paper",
      "Identifier": "3b2b5eca-409c-5cfb-9ac3-677d876ed3be",
      "Enabled": true,
      "MaxParticles": 400,
      "Places": 0,
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1",
      "Anchor": null,
      "Delay": 0.0,
      "Duration": 0.0,
      "PreWarm": 0.0,
      "TimeScale": 1,
      "Timing": "GameTime",
      "SpawnModules": [
        {
          "__type": "Rinten.SpawnBurstModule",
          "Stage": "Spawn",
          "Count": {
            "UseParameter": true,
            "Value": 160,
            "ParameterName": "Amount",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "34fb3586-f0b0-5b69-87a3-3b701048329c",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "Shape": "Point",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "363258ed-972b-536e-898a-e3ab19a4f3db",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeVelocityModule",
          "Stage": "Initialize",
          "Velocity": {
            "UseParameter": false,
            "Value": {
              "X": 0,
              "Y": 7,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": "Force",
            "IsBound": false
          },
          "Scatter": {
            "UseParameter": true,
            "Value": 6.0,
            "ParameterName": "Force",
            "Mode": "Multiply",
            "Multiplier": 1.0,
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
          "Identifier": "e97fa983-cfc6-589d-ac4e-660b67b436da",
          "Name": "Velocity",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": true,
            "Value": {
              "Type": "Range",
              "Evaluation": "Seed",
              "Constants": "3.0,4.5,0,0"
            },
            "ParameterName": "Lifetime",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "98abfda0-7ef2-5cca-b890-6808ed497c5e",
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
              "Constants": "0.08,0.13,0,0"
            },
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "32d86526-d9ff-5efd-8530-0097c8653678",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": {
              "Type": "Range",
              "Evaluation": "Particle",
              "ConstantA": "1.0000,0.1882,0.3765,1.0",
              "ConstantB": "0.1882,0.7529,1.0000,1.0"
            },
            "ParameterName": "Paper",
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "f8b011a5-6629-56ec-ab48-ba03fd407a18",
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
          "Identifier": "59578024-db9c-5268-b898-3adc5a21e66a",
          "Name": "Rotation",
          "Enabled": true
        },
        {
          "__type": "Rinten.ParticleCollisionModule",
          "Stage": "Initialize",
          "Ignore": "",
          "Radius": {
            "UseParameter": false,
            "Value": 0.03,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "DieOnHitChance": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Prefabs": [],
          "PrefabChance": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "PrefabRotation": {
            "UseParameter": false,
            "Value": 0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "PrefabAlign": false,
          "Bounce": {
            "UseParameter": false,
            "Value": 0.2,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Friction": {
            "UseParameter": false,
            "Value": 0.9,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Bumpiness": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "PushStrength": {
            "UseParameter": false,
            "Value": 0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "d194c995-4845-5163-9940-38f88e563c62",
          "Name": "Collision",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.EventModule",
          "Stage": "Update",
          "Trigger": "OnBirth",
          "At": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Every": 0.0,
          "Distance": 0.05,
          "Once": false,
          "Chance": 1.0,
          "Set": [
            {
              "Enabled": true,
              "Set": "Slot",
              "Slot": "Spin",
              "Value": {
                "UseParameter": false,
                "Value": {
                  "X": 1,
                  "Y": 1,
                  "Z": 1
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "W": {
                "UseParameter": false,
                "Value": 1.0,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Multiply": false
            }
          ],
          "Effect": null,
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToVelocity": false,
          "Follow": false,
          "MaxAlive": 16,
          "Context": [],
          "Identifier": "c12aea51-5bea-5151-85ed-cdf1ee03e3df",
          "Name": "Spin On",
          "Enabled": true
        },
        {
          "__type": "Rinten.EventModule",
          "Stage": "Update",
          "Trigger": "OnCollision",
          "At": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Every": 0.0,
          "Distance": 0.05,
          "Once": false,
          "Chance": 1.0,
          "Set": [
            {
              "Enabled": true,
              "Set": "Slot",
              "Slot": "Spin",
              "Value": {
                "UseParameter": false,
                "Value": {
                  "X": 0.3,
                  "Y": 0.3,
                  "Z": 0.3
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "W": {
                "UseParameter": false,
                "Value": 1.0,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Multiply": true
            }
          ],
          "Effect": null,
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToVelocity": false,
          "Follow": false,
          "MaxAlive": 16,
          "Context": [],
          "Identifier": "329c4f8d-3bf8-5d44-9019-1302441e8817",
          "Name": "Land",
          "Enabled": true
        },
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
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false,
            "SlotName": "Spin",
            "SlotMode": "Multiply"
          },
          "Identifier": "6fb3d58a-2014-5782-b29e-6bdc86c4981b",
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
              "Y": -9.8,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": "Gravity",
            "IsBound": false
          },
          "Identifier": "c72bd3d8-6495-5506-ad1d-54a2b86dd2bc",
          "Name": "Gravity",
          "Enabled": true
        },
        {
          "__type": "Rinten.DragModule",
          "Stage": "Update",
          "Damping": {
            "UseParameter": false,
            "Value": 0.6,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "23b89caa-8954-5fc0-bb4e-0e4d94fe3731",
          "Name": "Drag",
          "Enabled": true
        },
        {
          "__type": "Rinten.CurlNoiseModule",
          "Stage": "Update",
          "Strength": {
            "UseParameter": true,
            "Value": 2.0,
            "ParameterName": "Flutter",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "TimeScale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Offset": "0,0,0",
          "Identifier": "0527d4c0-ca86-5411-af07-469ceca46835",
          "Name": "Curl Noise",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/paper.sprite",
          "Scale": 1.0,
          "Alignment": "Particle",
          "FaceVelocity": false,
          "Additive": false,
          "Shadows": false,
          "Lighting": true,
          "DepthFeather": 0,
          "SortMode": "Unsorted",
          "Opaque": false,
          "FogStrength": 1.0,
          "TextureFilter": "Bilinear",
          "MotionBlur": false,
          "LeadingTrail": true,
          "BlurAmount": 0.5,
          "BlurSpacing": 0.5,
          "BlurOpacity": 0.5,
          "Identifier": "cdc77b75-f997-56de-9514-a64085d2f1e7",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Pop",
      "Identifier": "0539c28c-ed8e-594f-874e-0f9722d05335",
      "Enabled": true,
      "MaxParticles": 4,
      "Places": 0,
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1",
      "Anchor": null,
      "Delay": 0.0,
      "Duration": 0.0,
      "PreWarm": 0.0,
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
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "28908ea4-e84e-5fd5-9afb-d90d205dba89",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "Shape": "Point",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "0847232f-24ee-5cbf-b7b8-0d62e155cfcb",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 0.25,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "2e3eddb7-3bfe-5618-8b1d-c756f86365b6",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": {
                "rangey": "0,1.5",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.19999999999999998,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.7999999999999999,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,1.5",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.19999999999999998,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.7999999999999999,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              }
            },
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "6b19123a-dae3-5024-8632-e17b1eb0a433",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "1.0000,1.0000,1.0000,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": [
                {
                  "x": 0,
                  "y": 0.7,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 1,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                }
              ],
              "CurveB": [
                {
                  "x": 0,
                  "y": 0.7,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 1,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                }
              ]
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "8746db29-a1fa-5e23-a802-83fbbf7b0a1d",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/ring.sprite",
          "Scale": 1.0,
          "Alignment": "LookAtCamera",
          "FaceVelocity": false,
          "Additive": true,
          "Shadows": false,
          "Lighting": false,
          "DepthFeather": 0,
          "SortMode": "Unsorted",
          "Opaque": false,
          "FogStrength": 1.0,
          "TextureFilter": "Bilinear",
          "MotionBlur": false,
          "LeadingTrail": true,
          "BlurAmount": 0.5,
          "BlurSpacing": 0.5,
          "BlurOpacity": 0.5,
          "Identifier": "c1785d92-f3d2-50c8-ba0f-0a814e271648",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 4.0,
  "Looping": true,
  "Shapes": [],
  "Slots": [
    "Spin"
  ],
  "Anchors": [],
  "FloatParameters": [
    {
      "Name": "Amount",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "7b6e4d6f-92af-5ae7-aa7f-a340a6275f48"
    },
    {
      "Name": "Force",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "e5154372-b147-58d8-a1c3-803da37a8478"
    },
    {
      "Name": "Size",
      "DefaultValue": 1,
      "Min": 0.2,
      "Max": 3,
      "Identifier": "aa28643f-24dc-5d1d-8f12-1fa1d19f187c"
    },
    {
      "Name": "Lifetime",
      "DefaultValue": 1,
      "Min": 0.2,
      "Max": 3,
      "Identifier": "217a743c-8b19-5549-aa37-f2d90240fd19"
    },
    {
      "Name": "Gravity",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 3,
      "Identifier": "8520f75e-8aac-5714-a554-3bc190ebae0f"
    },
    {
      "Name": "Flutter",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "c836ebd6-4e41-5389-8728-9247bb8d062a"
    }
  ],
  "VectorParameters": [],
  "ColorParameters": [
    {
      "Name": "Paper",
      "DefaultValue": {
        "Type": "Range",
        "Evaluation": "Particle",
        "ConstantA": "1.0000,0.1882,0.3765,1.0",
        "ConstantB": "0.1882,0.7529,1.0000,1.0"
      },
      "Identifier": "fcc5dd9c-a60c-5082-86ea-ab4aabc5bf37"
    }
  ],
  "__references": [],
  "__version": 0
}