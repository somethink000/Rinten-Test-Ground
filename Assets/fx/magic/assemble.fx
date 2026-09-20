{
  "Emitters": [
    {
      "Name": "Shards",
      "Identifier": "7b263d08-1d43-5e09-bf63-f8107abde1d7",
      "Enabled": true,
      "MaxParticles": 48,
      "Places": 48,
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
            "Value": 48,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "dffdaa79-33e7-5f2f-b674-bbf618507ece",
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
          "Identifier": "eaf251ba-44ae-5f11-b944-893586f65f1a",
          "Name": "Position",
          "Enabled": true,
          "ShapeName": "Scatter",
          "Sample": "Random",
          "Along": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToShape": false
        },
        {
          "__type": "Rinten.InitializeVelocityModule",
          "Stage": "Initialize",
          "Velocity": {
            "UseParameter": false,
            "Value": {
              "X": 0,
              "Y": 0,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Scatter": {
            "UseParameter": false,
            "Value": 1.5,
            "ParameterName": null,
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
          "Identifier": "1d2f2f6a-aee3-5072-b89d-4a0ce419d326",
          "Name": "Velocity",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 4.2,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "01f9e19b-6243-517e-8102-e7372817b378",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.11,
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "8a076ebe-96c6-5c7e-92dc-201a062852ed",
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
          "Identifier": "7df50511-66b5-544b-8703-f2e16e80e956",
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
          "Identifier": "afda9e4f-4338-55eb-8816-acd2839505da",
          "Name": "Rotation",
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
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "f75f6f39-0891-5d6f-8f55-4be96e3be644",
          "Name": "Spin",
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
          "Identifier": "a6f49506-b633-5f53-847b-501e886eac83",
          "Name": "Drag",
          "Enabled": true
        },
        {
          "__type": "Rinten.GoalModule",
          "Stage": "Update",
          "Target": "Shape",
          "ShapeName": "Wall",
          "Sample": "ByIndex",
          "Along": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AnchorName": null,
          "Offset": "0,0,0",
          "SlotName": null,
          "PositionWeight": {
            "UseParameter": true,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": [
                {
                  "x": 0,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.12,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.45,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 1,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                }
              ],
              "CurveB": [
                {
                  "x": 0,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.12,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.45,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 1,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                }
              ]
            },
            "ParameterName": "Gather",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "RotationWeight": {
            "UseParameter": true,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": [
                {
                  "x": 0,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.12,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.45,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 1,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                }
              ],
              "CurveB": [
                {
                  "x": 0,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.12,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.45,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 1,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                }
              ]
            },
            "ParameterName": "Gather",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "ScaleWeight": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToMotion": false,
          "WriteVelocity": true,
          "Identifier": "4ad8094c-2b64-5c8a-9c2c-0a09b090b613",
          "Name": "Goal",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/box.mdl",
          "Material": "materials/fx/stylized_ember.mat",
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "RotateWithObject": false,
          "CastShadows": false,
          "PartFromParticle": false,
          "Morphs": [],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
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
                      "x": 0.3,
                      "y": 0.05,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.8,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.92,
                      "y": 0.5,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1,
                      "y": 1.0,
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
                      "x": 0.3,
                      "y": 0.05,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.8,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.92,
                      "y": 0.5,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1,
                      "y": 1.0,
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
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Edge",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.15,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Emission",
              "Width": 1,
              "Value": {
                "UseParameter": true,
                "Value": {
                  "Type": "Curve",
                  "Evaluation": "Life",
                  "CurveA": {
                    "rangey": "0,4",
                    "frames": [
                      {
                        "x": 0,
                        "y": 0.75,
                        "in": 0,
                        "out": 0,
                        "mode": "Flat"
                      },
                      {
                        "x": 0.45,
                        "y": 0.3,
                        "in": 0,
                        "out": 0,
                        "mode": "Flat"
                      },
                      {
                        "x": 0.8,
                        "y": 0.25,
                        "in": 0,
                        "out": 0,
                        "mode": "Flat"
                      },
                      {
                        "x": 1,
                        "y": 0.875,
                        "in": 0,
                        "out": 0,
                        "mode": "Flat"
                      }
                    ]
                  },
                  "CurveB": {
                    "rangey": "0,4",
                    "frames": [
                      {
                        "x": 0,
                        "y": 0.75,
                        "in": 0,
                        "out": 0,
                        "mode": "Flat"
                      },
                      {
                        "x": 0.45,
                        "y": 0.3,
                        "in": 0,
                        "out": 0,
                        "mode": "Flat"
                      },
                      {
                        "x": 0.8,
                        "y": 0.25,
                        "in": 0,
                        "out": 0,
                        "mode": "Flat"
                      },
                      {
                        "x": 1,
                        "y": 0.875,
                        "in": 0,
                        "out": 0,
                        "mode": "Flat"
                      }
                    ]
                  }
                },
                "ParameterName": "Glow",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Scroll",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.6,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            }
          ],
          "ParticleAttributes": true,
          "Identifier": "0aa4d953-8bcf-5a0a-9a5c-87f02041bade",
          "Name": "Mesh",
          "Enabled": true
        },
        {
          "__type": "Rinten.SpawnEffectOnDeathModule",
          "Stage": "Render",
          "Effect": "fx/fireworks/crackle.fx",
          "Chance": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Scale": {
            "UseParameter": false,
            "Value": 0.4,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToVelocity": false,
          "OnCollision": false,
          "OnExpiry": true,
          "MaxAlive": 16,
          "Identifier": "717b9de9-8e84-564a-a926-93da8b5c971f",
          "Name": "Effect On Death",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Lock Flash",
      "Identifier": "2e958910-3cc3-58b2-b29e-3d4ddcdde70d",
      "Enabled": true,
      "MaxParticles": 1,
      "Places": 0,
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1",
      "Anchor": null,
      "Delay": 1.9,
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
          "Identifier": "39697728-9f08-5dd6-a0ad-bce147e2819b",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "Shape": "Point",
          "Offset": "0,1.5,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "166a82fc-dd05-5cb4-a20b-015475682e1b",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 0.35,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "0c203ea4-320c-5089-bd87-c472d6174d4d",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": {
                "rangey": "0,3",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.16666666666666666,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.8666666666666667,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,3",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.16666666666666666,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.8666666666666667,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              }
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "d651a8f4-61aa-5bf0-b804-bd5119c7af2a",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "1.0000,0.8157,0.6275,1.0",
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
                  "y": 0.8,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                },
                {
                  "x": 1,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                }
              ],
              "CurveB": [
                {
                  "x": 0,
                  "y": 0.8,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                },
                {
                  "x": 1,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
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
            "Value": 1.5,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "aa4619bf-5204-5468-8999-22016136e248",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/glow.sprite",
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
          "Identifier": "f59cd6c8-be0c-5b1f-87c5-dde2397e44b8",
          "Name": "Sprite",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "1.0000,0.5647,0.2510,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 10,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Radius": {
            "UseParameter": false,
            "Value": 5,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Attenuation": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "MaxLights": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Ratio": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "UseParticleColor": false,
          "CastShadows": false,
          "Identifier": "689659d2-ac31-5649-b917-463950862e7f",
          "Name": "Light",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Dust",
      "Identifier": "30f7acb9-ac35-53a6-b21f-d0d9f6188f64",
      "Enabled": true,
      "MaxParticles": 60,
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
          "__type": "Rinten.SpawnRateModule",
          "Stage": "Spawn",
          "Rate": {
            "UseParameter": false,
            "Value": 25,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "442262ec-d314-58eb-a590-8de0adc5ae9e",
          "Name": "Spawn Rate",
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
          "Identifier": "213fd1bc-3787-5ec3-b9d6-135fa081357b",
          "Name": "Position",
          "Enabled": true,
          "ShapeName": "Scatter",
          "Sample": "Random",
          "Along": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToShape": false
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": {
              "Type": "Range",
              "Evaluation": "Seed",
              "Constants": "1.0,2.0,0,0"
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "62e285e4-e0eb-5f5e-9541-a3a65f92b663",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": {
              "Type": "Range",
              "Evaluation": "Seed",
              "Constants": "0.015,0.03,0,0"
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "02caf386-537b-5be9-a904-630040735cbc",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "1.0000,0.7529,0.5020,1.0",
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
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.3,
                  "y": 0.6,
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
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.3,
                  "y": 0.6,
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
            "Value": 1.2,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "5671faaf-5d47-5f1b-b2d8-494000a1a9a5",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/dot.sprite",
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
          "Identifier": "9647f01e-eddc-5184-8445-12925d9cae20",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 4.4,
  "Looping": true,
  "Shapes": [
    {
      "Name": "Scatter",
      "Identifier": "e6dd0752-9879-5bd1-b9eb-9b2b7e6addf6",
      "Kind": "Sphere",
      "Anchor": null,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1.0,
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Offset": "0,1.5,0",
      "Rotation": "0,0,0",
      "Radius": 2.2,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": false,
      "LineStart": "0,0,0",
      "LineEnd": "0,1,0",
      "Points": [],
      "Closed": false,
      "GridCount": "5,1,5",
      "GridSpacing": "0.3,0.3,0.3",
      "Height": 2.0,
      "Turns": 3.0,
      "Count": 0
    },
    {
      "Name": "Wall",
      "Identifier": "260f921d-1add-5968-82ef-992814d3f96a",
      "Kind": "Grid",
      "Anchor": null,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1.0,
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Offset": "0,1.5,0",
      "Rotation": "0,0,0",
      "Radius": 0.5,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": false,
      "LineStart": "0,0,0",
      "LineEnd": "0,1,0",
      "Points": [],
      "Closed": false,
      "GridCount": "8,6,1",
      "GridSpacing": "0.24,0.24,0.24",
      "Height": 2.0,
      "Turns": 3.0,
      "Count": 0
    }
  ],
  "Slots": [],
  "Anchors": [],
  "FloatParameters": [
    {
      "Name": "Gather",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 1,
      "Identifier": "ff7d6819-f9fc-50f3-8fce-491e6879ff7e"
    },
    {
      "Name": "Glow",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 3,
      "Identifier": "6e941755-ba13-5f6b-b668-a3913c5a96a2"
    },
    {
      "Name": "Size",
      "DefaultValue": 1,
      "Min": 0.2,
      "Max": 3,
      "Identifier": "aa28643f-24dc-5d1d-8f12-1fa1d19f187c"
    }
  ],
  "VectorParameters": [],
  "ColorParameters": [],
  "__references": [],
  "__version": 0
}