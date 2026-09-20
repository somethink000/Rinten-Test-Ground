{
  "Emitters": [
    {
      "Name": "Body",
      "Identifier": "5e4bdf37-fbc2-54b7-9a45-095c9f2abf05",
      "Enabled": true,
      "MaxParticles": 1,
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
          "Identifier": "ab4a658c-9972-53bc-938d-83fcf99bd277",
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
          "Identifier": "14ecd89c-385f-5199-8e40-ffab2f685dbc",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 10000.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "e7594073-7c2c-5d99-a139-da45670dfad2",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": 2.6,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "3577ae5b-322e-5744-8d66-eaab7b85148f",
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
          "Identifier": "39ddb37b-4436-5c6f-a363-f363faaa0386",
          "Name": "Color",
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
              "X": 0,
              "Y": 0.0,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "296e333c-0420-5383-b145-8d3668cf092d",
          "Name": "Spin",
          "Enabled": true
        },
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Centre",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Speed": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Stagger": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Loop": true,
          "Weight": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToShape": false,
          "Identifier": "5f6eeda4-c55a-5ff3-af13-c752ce5c11a5",
          "Name": "Follow Shape",
          "Enabled": true
        },
        {
          "__type": "Rinten.EventModule",
          "Stage": "Update",
          "Trigger": "EveryStep",
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
              "Set": "Anchor",
              "Slot": null,
              "Value": {
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
              "W": {
                "UseParameter": false,
                "Value": 1.0,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Multiply": false,
              "AnchorName": "Planet"
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
          "Identifier": "8d13bade-eed3-5eb3-b9f6-5ab79384f1df",
          "Name": "Publish Planet",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/sphere.mdl",
          "Material": "materials/solar/jupiter.mat",
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "RotateWithObject": false,
          "CastShadows": true,
          "PartFromParticle": false,
          "Morphs": [],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Emission",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 1.0,
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
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.0,
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
              "Name": "Shadow",
              "Width": 3,
              "Value": {
                "UseParameter": false,
                "Value": 0,
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
              "AsVector": true,
              "Vector": {
                "UseParameter": true,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": "Io",
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            }
          ],
          "ParticleAttributes": true,
          "Identifier": "d3099c57-e38f-52a1-92ef-b1ffca60b31e",
          "Name": "Mesh",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Juno",
      "Identifier": "307f8ad2-60d6-58e5-9c6b-0b3b2bf40011",
      "Enabled": true,
      "MaxParticles": 1,
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
          "Identifier": "3e15a4dd-30b4-5737-9382-426cf592ca4a",
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
          "Identifier": "eac33fcf-9954-583b-b7a1-6a2512a53387",
          "Name": "Position",
          "Enabled": true,
          "ShapeName": "Polar",
          "Sample": "ByTime",
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
            "Value": 10000.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "63c55c71-c3e5-5f5d-8140-eec9d6f9ded8",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": 0.1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "158024da-0c33-51ed-9a74-42809ca93f12",
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
          "Identifier": "7a7bf8cb-09f2-5357-b76e-437cc0bae38f",
          "Name": "Color",
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
              "X": 4.5,
              "Y": 15.0,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "28e09da2-cb52-572c-a05f-bc6493c1d3d4",
          "Name": "Spin",
          "Enabled": true
        },
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Polar",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Speed": {
            "UseParameter": true,
            "Value": 0.09090909090909091,
            "ParameterName": "Speed",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Stagger": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Loop": true,
          "Weight": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToShape": false,
          "Identifier": "dd249009-c6d6-5908-b165-03b1701e1e38",
          "Name": "Follow Shape",
          "Enabled": true
        },
        {
          "__type": "Rinten.EventModule",
          "Stage": "Update",
          "Trigger": "EveryStep",
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
              "Set": "Anchor",
              "Slot": null,
              "Value": {
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
              "W": {
                "UseParameter": false,
                "Value": 1.0,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Multiply": false,
              "AnchorName": "Juno"
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
          "Identifier": "eb024ff4-d029-5f7e-b6fe-de584bab0d0b",
          "Name": "Publish Juno",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/space/juno.mdl",
          "Material": null,
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "RotateWithObject": false,
          "CastShadows": true,
          "PartFromParticle": false,
          "Morphs": [],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Emission",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 1.0,
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
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.0,
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
          "ParticleAttributes": false,
          "Identifier": "67e417af-e83b-5a7c-8fb5-c89a42d19096",
          "Name": "Mesh",
          "Enabled": true
        },
        {
          "__type": "Rinten.TrailRenderModule",
          "Stage": "Render",
          "Material": null,
          "Width": {
            "UseParameter": false,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": {
                "rangey": "0,0.025",
                "frames": [
                  {
                    "x": 0,
                    "y": 1.0,
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
              "CurveB": {
                "rangey": "0,0.025",
                "frames": [
                  {
                    "x": 0,
                    "y": 1.0,
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
              }
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
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
                    "c": "0.7529,0.8784,1.0000,0.4"
                  },
                  {
                    "t": 1,
                    "c": "0.7529,0.8784,1.0000,0.4"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.4
                  },
                  {
                    "t": 1,
                    "a": 0.0
                  }
                ]
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "0.7529,0.8784,1.0000,0.4"
                  },
                  {
                    "t": 1,
                    "c": "0.7529,0.8784,1.0000,0.4"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.4
                  },
                  {
                    "t": 1,
                    "a": 0.0
                  }
                ]
              }
            },
            "ParameterName": null,
            "IsBound": false
          },
          "UnitsPerTexture": 0.5,
          "Scroll": 0,
          "MaxPoints": 40,
          "PointDistance": 0.02,
          "LifeTime": 1.65,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": false,
          "TintFromParticle": false,
          "Identifier": "28593325-d92d-52f1-a45d-673d195bfd70",
          "Name": "Trail",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Haze",
      "Identifier": "a1d5f8db-04a6-5cb1-820d-0edb09b60306",
      "Enabled": true,
      "MaxParticles": 6,
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
            "Value": 3,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "9e13b4a5-5783-509c-948d-9bb4d6707339",
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
          "Identifier": "29c5328d-c61a-5af0-b393-b113dd486098",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLocalSpaceModule",
          "Stage": "Initialize",
          "LocalSpace": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "24792835-71d7-5f59-8801-c60c5fe6e61e",
          "Name": "Local Space",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "dc10c02d-10dd-5eba-81cc-738adbd3c3ac",
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
                "rangey": "0,3.25",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.9600000000000001,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 0.5,
                    "y": 1.0,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.9600000000000001,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,3.25",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.9600000000000001,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 0.5,
                    "y": 1.0,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.9600000000000001,
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
          "Identifier": "9cb1e954-3b3d-5c9e-8bbf-c71cc6d3053f",
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
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.5,
                  "y": 0.06,
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
                  "x": 0.5,
                  "y": 0.06,
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
          "Identifier": "68eaa46c-9051-56f8-a844-958d1b30b952",
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
          "Identifier": "eb8e6ecd-229b-5092-b465-e213e44dc571",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Atmosphere",
      "Identifier": "8d140a3b-0d8a-5de4-8e04-6c1a61a573a3",
      "Enabled": true,
      "MaxParticles": 1,
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
          "Identifier": "0c85abbe-29e9-5324-b829-2c13cc2f4115",
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
          "Identifier": "fb5634e2-3fa3-5143-98d3-133253f34976",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 10000.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "2524f40c-35e0-5949-9783-49e842296656",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": 2.7560000000000002,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "850562d3-fe4b-5526-bc4b-569a9e25751c",
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
          "Identifier": "8e97839b-c5e6-5144-bfa8-8650ec434aca",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Centre",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Speed": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Stagger": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Loop": true,
          "Weight": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToShape": false,
          "Identifier": "dd012b9a-45f1-54bb-b175-46ba87c1ee7c",
          "Name": "Follow Shape",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/sphere.mdl",
          "Material": "materials/solar/jupiter_atmo.mat",
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
              "Name": "Emission",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 1.0,
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
          "ParticleAttributes": false,
          "Identifier": "0acbe623-a03d-5f95-ba5e-2f94e9126363",
          "Name": "Mesh",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Io",
      "Identifier": "05b116a4-a12d-56f9-81f4-886014682d50",
      "Enabled": true,
      "MaxParticles": 1,
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
          "Identifier": "a0bdb413-b159-545e-a2e2-8e3ec32ed2c4",
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
          "Identifier": "9d299b63-c3c0-5ed1-9ecd-e3d2a25ea2c9",
          "Name": "Position",
          "Enabled": true,
          "ShapeName": "Orbit Io",
          "Sample": "ByTime",
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
            "Value": 10000.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "1c0384cc-abca-5e04-b831-f270a7358f38",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": 0.2,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "f02b608c-230b-502f-a8c6-33909aee08e4",
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
          "Identifier": "685f46b5-5c90-5d05-bb2e-7224454d2da7",
          "Name": "Color",
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
              "X": 0,
              "Y": 40.0,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "bb081893-1c83-5f99-b6b1-106c2f1a1a5a",
          "Name": "Spin",
          "Enabled": true
        },
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Orbit Io",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Speed": {
            "UseParameter": true,
            "Value": 0.1111111111111111,
            "ParameterName": "Speed",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Stagger": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Loop": true,
          "Weight": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToShape": false,
          "Identifier": "9ddd275c-2cc6-5a7a-95f5-b4886196b819",
          "Name": "Follow Shape",
          "Enabled": true
        },
        {
          "__type": "Rinten.EventModule",
          "Stage": "Update",
          "Trigger": "EveryStep",
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
              "Set": "Anchor",
              "Slot": null,
              "Value": {
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
              "W": {
                "UseParameter": false,
                "Value": 1.0,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Multiply": false,
              "AnchorName": "Io"
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
          "Identifier": "635f5674-be32-5048-8f03-d8bf9cbd9e6d",
          "Name": "Publish Io",
          "Enabled": true
        },
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
          "Set": [],
          "Effect": "fx/solar/io_plumes.fx",
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToVelocity": false,
          "Follow": true,
          "MaxAlive": 1,
          "Context": [],
          "Identifier": "a41647d4-7078-5c70-8d4d-16aab4a3e41d",
          "Name": "Rides",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/sphere.mdl",
          "Material": "materials/solar/io.mat",
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "RotateWithObject": false,
          "CastShadows": true,
          "PartFromParticle": false,
          "Morphs": [],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Emission",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 1.0,
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
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.0,
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
              "Name": "Shadow",
              "Width": 3,
              "Value": {
                "UseParameter": false,
                "Value": 0,
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
              "AsVector": true,
              "Vector": {
                "UseParameter": true,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": "Planet",
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            }
          ],
          "ParticleAttributes": true,
          "Identifier": "1bbe5e2f-ef24-508d-8467-deefabcf2199",
          "Name": "Mesh",
          "Enabled": true
        },
        {
          "__type": "Rinten.TrailRenderModule",
          "Stage": "Render",
          "Material": null,
          "Width": {
            "UseParameter": false,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": {
                "rangey": "0,0.06999999999999999",
                "frames": [
                  {
                    "x": 0,
                    "y": 1.0,
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
              "CurveB": {
                "rangey": "0,0.06999999999999999",
                "frames": [
                  {
                    "x": 0,
                    "y": 1.0,
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
              }
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
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
                    "c": "1.0000,1.0000,1.0000,0.25"
                  },
                  {
                    "t": 1,
                    "c": "1.0000,1.0000,1.0000,0.25"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.25
                  },
                  {
                    "t": 1,
                    "a": 0.0
                  }
                ]
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "1.0000,1.0000,1.0000,0.25"
                  },
                  {
                    "t": 1,
                    "c": "1.0000,1.0000,1.0000,0.25"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.25
                  },
                  {
                    "t": 1,
                    "a": 0.0
                  }
                ]
              }
            },
            "ParameterName": null,
            "IsBound": false
          },
          "UnitsPerTexture": 0.5,
          "Scroll": 0,
          "MaxPoints": 48,
          "PointDistance": 0.03,
          "LifeTime": 1.08,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": false,
          "TintFromParticle": false,
          "Identifier": "63e3f9b6-cce4-5732-93c4-81383879b23b",
          "Name": "Trail",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Europa",
      "Identifier": "ebc031d3-dc1a-5de3-a9c1-07b6282f0ad1",
      "Enabled": true,
      "MaxParticles": 1,
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
          "Identifier": "2a1b3c5b-baa5-539e-bfa8-48dd5046b91d",
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
          "Identifier": "b9ed2e2f-8299-5452-9dd5-e8faf94e9370",
          "Name": "Position",
          "Enabled": true,
          "ShapeName": "Orbit Europa",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": false,
            "Value": 0.3,
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
            "Value": 10000.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "2959cf97-9be7-5f74-93ec-a613a5c5349e",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": 0.18,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "d857888b-63bc-5211-a287-2d5a084ba5e0",
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
          "Identifier": "683f8699-03f0-5f45-b213-0655244cc76d",
          "Name": "Color",
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
              "X": 0,
              "Y": 25.714285714285715,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "e7403f7f-48da-5710-a993-6cc461f6a1e8",
          "Name": "Spin",
          "Enabled": true
        },
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Orbit Europa",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": false,
            "Value": 0.3,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Speed": {
            "UseParameter": true,
            "Value": 0.07142857142857142,
            "ParameterName": "Speed",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Stagger": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Loop": true,
          "Weight": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToShape": false,
          "Identifier": "a787d23e-09ef-5f4f-be36-8fa4afbdce9e",
          "Name": "Follow Shape",
          "Enabled": true
        },
        {
          "__type": "Rinten.EventModule",
          "Stage": "Update",
          "Trigger": "EveryStep",
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
              "Set": "Anchor",
              "Slot": null,
              "Value": {
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
              "W": {
                "UseParameter": false,
                "Value": 1.0,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Multiply": false,
              "AnchorName": "Europa"
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
          "Identifier": "49db44f3-e5ab-55d3-8282-c5d6597434fa",
          "Name": "Publish Europa",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/sphere.mdl",
          "Material": "materials/solar/europa.mat",
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "RotateWithObject": false,
          "CastShadows": true,
          "PartFromParticle": false,
          "Morphs": [],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Emission",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 1.0,
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
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.0,
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
              "Name": "Shadow",
              "Width": 3,
              "Value": {
                "UseParameter": false,
                "Value": 0,
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
              "AsVector": true,
              "Vector": {
                "UseParameter": true,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": "Planet",
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            }
          ],
          "ParticleAttributes": true,
          "Identifier": "fea91270-c2d4-557f-ad5e-c9e123a41aaa",
          "Name": "Mesh",
          "Enabled": true
        },
        {
          "__type": "Rinten.TrailRenderModule",
          "Stage": "Render",
          "Material": null,
          "Width": {
            "UseParameter": false,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": {
                "rangey": "0,0.063",
                "frames": [
                  {
                    "x": 0,
                    "y": 1.0,
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
              "CurveB": {
                "rangey": "0,0.063",
                "frames": [
                  {
                    "x": 0,
                    "y": 1.0,
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
              }
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
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
                    "c": "1.0000,1.0000,1.0000,0.25"
                  },
                  {
                    "t": 1,
                    "c": "1.0000,1.0000,1.0000,0.25"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.25
                  },
                  {
                    "t": 1,
                    "a": 0.0
                  }
                ]
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "1.0000,1.0000,1.0000,0.25"
                  },
                  {
                    "t": 1,
                    "c": "1.0000,1.0000,1.0000,0.25"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.25
                  },
                  {
                    "t": 1,
                    "a": 0.0
                  }
                ]
              }
            },
            "ParameterName": null,
            "IsBound": false
          },
          "UnitsPerTexture": 0.5,
          "Scroll": 0,
          "MaxPoints": 48,
          "PointDistance": 0.03,
          "LifeTime": 1.68,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": false,
          "TintFromParticle": false,
          "Identifier": "d3d86645-228c-536f-891a-4497773e4e32",
          "Name": "Trail",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Ganymede",
      "Identifier": "41b12dfb-79dc-516f-8a5c-ceaf85bfb4a7",
      "Enabled": true,
      "MaxParticles": 1,
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
          "Identifier": "8da549bc-2351-5aa5-978b-8fb3b8a9c1bf",
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
          "Identifier": "9043d20d-75f1-537c-9012-f6224710da03",
          "Name": "Position",
          "Enabled": true,
          "ShapeName": "Orbit Ganymede",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": false,
            "Value": 0.6,
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
            "Value": 10000.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "662fb7e2-ec51-5ae8-9644-0f75a35b5180",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": 0.28,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "0ab7ff5a-ccd6-5323-9380-aaf666cec4e3",
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
          "Identifier": "07c8fa09-54f3-53d2-b700-6660c3cf7eca",
          "Name": "Color",
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
              "X": 0,
              "Y": 16.363636363636363,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "360d593b-49ef-58f5-950e-bd72824fae17",
          "Name": "Spin",
          "Enabled": true
        },
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Orbit Ganymede",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": false,
            "Value": 0.6,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Speed": {
            "UseParameter": true,
            "Value": 0.045454545454545456,
            "ParameterName": "Speed",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Stagger": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Loop": true,
          "Weight": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToShape": false,
          "Identifier": "1e91c766-a389-5797-8568-3a53e690783f",
          "Name": "Follow Shape",
          "Enabled": true
        },
        {
          "__type": "Rinten.EventModule",
          "Stage": "Update",
          "Trigger": "EveryStep",
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
              "Set": "Anchor",
              "Slot": null,
              "Value": {
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
              "W": {
                "UseParameter": false,
                "Value": 1.0,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Multiply": false,
              "AnchorName": "Ganymede"
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
          "Identifier": "0d308968-0833-50b1-87b2-7ef9b7607f1a",
          "Name": "Publish Ganymede",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/sphere.mdl",
          "Material": "materials/solar/moon.mat",
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "RotateWithObject": false,
          "CastShadows": true,
          "PartFromParticle": false,
          "Morphs": [],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Emission",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 1.0,
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
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.0,
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
              "Name": "Shadow",
              "Width": 3,
              "Value": {
                "UseParameter": false,
                "Value": 0,
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
              "AsVector": true,
              "Vector": {
                "UseParameter": true,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": "Planet",
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            }
          ],
          "ParticleAttributes": true,
          "Identifier": "a94eb571-650a-5c17-b3c5-03c2c8c034f5",
          "Name": "Mesh",
          "Enabled": true
        },
        {
          "__type": "Rinten.TrailRenderModule",
          "Stage": "Render",
          "Material": null,
          "Width": {
            "UseParameter": false,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": {
                "rangey": "0,0.098",
                "frames": [
                  {
                    "x": 0,
                    "y": 1.0,
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
              "CurveB": {
                "rangey": "0,0.098",
                "frames": [
                  {
                    "x": 0,
                    "y": 1.0,
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
              }
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
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
                    "c": "1.0000,1.0000,1.0000,0.25"
                  },
                  {
                    "t": 1,
                    "c": "1.0000,1.0000,1.0000,0.25"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.25
                  },
                  {
                    "t": 1,
                    "a": 0.0
                  }
                ]
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "1.0000,1.0000,1.0000,0.25"
                  },
                  {
                    "t": 1,
                    "c": "1.0000,1.0000,1.0000,0.25"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.25
                  },
                  {
                    "t": 1,
                    "a": 0.0
                  }
                ]
              }
            },
            "ParameterName": null,
            "IsBound": false
          },
          "UnitsPerTexture": 0.5,
          "Scroll": 0,
          "MaxPoints": 48,
          "PointDistance": 0.03,
          "LifeTime": 2.6399999999999997,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": false,
          "TintFromParticle": false,
          "Identifier": "4bb1a5d1-3284-5b22-9ff3-605bdec05817",
          "Name": "Trail",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Callisto",
      "Identifier": "c0b37026-3694-5359-825a-5a8743da172c",
      "Enabled": true,
      "MaxParticles": 1,
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
          "Identifier": "b60bb71b-1cac-59dd-96f4-ae75a5417359",
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
          "Identifier": "87709a64-febe-5e0d-bef0-1c24c38a4c3a",
          "Name": "Position",
          "Enabled": true,
          "ShapeName": "Orbit Callisto",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": false,
            "Value": 0.85,
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
            "Value": 10000.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "e10a110f-0313-5b92-898d-87c19f159be7",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": 0.26,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "a782ece4-fefe-5f6f-92a2-26de363f9108",
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
          "Identifier": "aea460d5-dcc5-554b-9ca5-6bf3983a481f",
          "Name": "Color",
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
              "X": 0,
              "Y": 10.0,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "52b47137-c986-54fb-b5fe-3bcd32493a4f",
          "Name": "Spin",
          "Enabled": true
        },
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Orbit Callisto",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": false,
            "Value": 0.85,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Speed": {
            "UseParameter": true,
            "Value": 0.027777777777777776,
            "ParameterName": "Speed",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Stagger": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Loop": true,
          "Weight": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToShape": false,
          "Identifier": "0152b778-22f2-5701-9270-1e94c5d43e99",
          "Name": "Follow Shape",
          "Enabled": true
        },
        {
          "__type": "Rinten.EventModule",
          "Stage": "Update",
          "Trigger": "EveryStep",
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
              "Set": "Anchor",
              "Slot": null,
              "Value": {
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
              "W": {
                "UseParameter": false,
                "Value": 1.0,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Multiply": false,
              "AnchorName": "Callisto"
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
          "Identifier": "eb7720f1-1518-54c7-adf1-14990897e38b",
          "Name": "Publish Callisto",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/sphere.mdl",
          "Material": "materials/solar/mercury.mat",
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "RotateWithObject": false,
          "CastShadows": true,
          "PartFromParticle": false,
          "Morphs": [],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Emission",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 1.0,
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
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.0,
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
              "Name": "Shadow",
              "Width": 3,
              "Value": {
                "UseParameter": false,
                "Value": 0,
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
              "AsVector": true,
              "Vector": {
                "UseParameter": true,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": "Planet",
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            }
          ],
          "ParticleAttributes": true,
          "Identifier": "26574e6d-5819-5fea-8e66-0555dfb84446",
          "Name": "Mesh",
          "Enabled": true
        },
        {
          "__type": "Rinten.TrailRenderModule",
          "Stage": "Render",
          "Material": null,
          "Width": {
            "UseParameter": false,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": {
                "rangey": "0,0.091",
                "frames": [
                  {
                    "x": 0,
                    "y": 1.0,
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
              "CurveB": {
                "rangey": "0,0.091",
                "frames": [
                  {
                    "x": 0,
                    "y": 1.0,
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
              }
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
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
                    "c": "1.0000,1.0000,1.0000,0.25"
                  },
                  {
                    "t": 1,
                    "c": "1.0000,1.0000,1.0000,0.25"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.25
                  },
                  {
                    "t": 1,
                    "a": 0.0
                  }
                ]
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "1.0000,1.0000,1.0000,0.25"
                  },
                  {
                    "t": 1,
                    "c": "1.0000,1.0000,1.0000,0.25"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.25
                  },
                  {
                    "t": 1,
                    "a": 0.0
                  }
                ]
              }
            },
            "ParameterName": null,
            "IsBound": false
          },
          "UnitsPerTexture": 0.5,
          "Scroll": 0,
          "MaxPoints": 48,
          "PointDistance": 0.03,
          "LifeTime": 4.32,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": false,
          "TintFromParticle": false,
          "Identifier": "794d0ee0-dbb0-5d80-9e95-b462f45c9b1e",
          "Name": "Trail",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Ring 0.0",
      "Identifier": "ba7ba351-066c-54fb-a98d-43523268d12f",
      "Enabled": true,
      "MaxParticles": 160,
      "Places": 160,
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
            "Value": 160,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "8f798559-c51c-5071-9973-ef721c5ccd4b",
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
          "Identifier": "1afed0d2-102d-57e8-822f-e4c8b3aee962",
          "Name": "Position",
          "Enabled": true,
          "ShapeName": "Ring 0.0",
          "Sample": "ByIndex",
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
            "Value": 10000.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "961f72f7-e7bc-51d1-a698-7b3319810c9f",
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
              "Constants": "0.015,0.034999999999999996,0,0"
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "243be6e9-6a4a-560e-b803-c9a3844b7d46",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.6902,0.6275,0.5647,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": 0.3,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 1.1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "311cf23b-7259-5474-b5c1-45a3e14b1e33",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Ring 0.0",
          "Sample": "ByIndex",
          "Along": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Speed": {
            "UseParameter": true,
            "Value": 0.019375,
            "ParameterName": "Speed",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Stagger": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Loop": true,
          "Weight": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToShape": false,
          "Identifier": "85e1b8c5-3425-55d7-aa8c-a3cffaad720a",
          "Name": "Follow Shape",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/dot.sprite",
          "Scale": 1.0,
          "Alignment": "LookAtCamera",
          "FaceVelocity": false,
          "Additive": false,
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
          "Identifier": "f273e7f6-181f-58bc-92e6-c89eea9ea3b4",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Ring 0.1",
      "Identifier": "fadda3c4-dc8a-5ddd-b24e-59fee5eb5c32",
      "Enabled": true,
      "MaxParticles": 160,
      "Places": 160,
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
            "Value": 160,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "f931826d-4ad9-545d-a72b-a37476b5e7b8",
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
          "Identifier": "d613da25-04bb-56b6-95cc-716d5ce97095",
          "Name": "Position",
          "Enabled": true,
          "ShapeName": "Ring 0.1",
          "Sample": "ByIndex",
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
            "Value": 10000.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "6b480366-bff6-50ca-8a9e-7d8a1d229056",
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
              "Constants": "0.015,0.034999999999999996,0,0"
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "17cd5039-efd7-5c86-a429-8f3d3b81a025",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.6902,0.6275,0.5647,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": 0.3,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 1.1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "a3985e69-d5a4-52ff-983e-749b4d8682c4",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Ring 0.1",
          "Sample": "ByIndex",
          "Along": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Speed": {
            "UseParameter": true,
            "Value": 0.01823529411764706,
            "ParameterName": "Speed",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Stagger": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Loop": true,
          "Weight": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToShape": false,
          "Identifier": "e17ee167-b0b3-54f7-ab05-e3a3357a0d45",
          "Name": "Follow Shape",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/dot.sprite",
          "Scale": 1.0,
          "Alignment": "LookAtCamera",
          "FaceVelocity": false,
          "Additive": false,
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
          "Identifier": "5132e638-eecb-50c1-a68e-6bc8f0ea9132",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 10,
  "Looping": true,
  "Shapes": [
    {
      "Name": "Centre",
      "Identifier": "f9a5d20c-45a0-5429-9d76-cf72ae1a6f86",
      "Kind": "Point",
      "Anchor": null,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1.0,
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Radius": 0.5,
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
      "Name": "Polar",
      "Identifier": "8e328a46-022c-55ed-9279-70d1257c0d71",
      "Kind": "Circle",
      "Anchor": null,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1.0,
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Offset": "0,0,0",
      "Rotation": "90.0,0,0",
      "Radius": 1.9,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": true,
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
      "Name": "Orbit Io",
      "Identifier": "35bf2420-2bb7-5623-accf-456add254b3b",
      "Kind": "Circle",
      "Anchor": null,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1.0,
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Offset": "0,0,0",
      "Rotation": "1.0,0,0",
      "Radius": 2.2,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": true,
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
      "Name": "Orbit Europa",
      "Identifier": "57b1bd06-1bbd-5ee0-b661-5874036cd3b9",
      "Kind": "Circle",
      "Anchor": null,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1.0,
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Offset": "0,0,0",
      "Rotation": "0.5,0,0",
      "Radius": 2.8,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": true,
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
      "Name": "Orbit Ganymede",
      "Identifier": "f4e43a7c-46d0-5227-88e2-5dc0f9ef0a9e",
      "Kind": "Circle",
      "Anchor": null,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1.0,
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Offset": "0,0,0",
      "Rotation": "0.2,0,0",
      "Radius": 3.5,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": true,
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
      "Name": "Orbit Callisto",
      "Identifier": "b713d96b-4e46-58a9-bb4d-d538e34d0737",
      "Kind": "Circle",
      "Anchor": null,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1.0,
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Offset": "0,0,0",
      "Rotation": "0.3,0,0",
      "Radius": 4.4,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": true,
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
      "Name": "Ring 0.0",
      "Identifier": "3f69276c-fae3-5d58-ad4d-683bc691852a",
      "Kind": "Circle",
      "Anchor": null,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1.0,
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Offset": "0,0,0",
      "Rotation": "3.0,0,0",
      "Radius": 1.6,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": true,
      "LineStart": "0,0,0",
      "LineEnd": "0,1,0",
      "Points": [],
      "Closed": false,
      "GridCount": "5,1,5",
      "GridSpacing": "0.3,0.3,0.3",
      "Height": 2.0,
      "Turns": 3.0,
      "Count": 160
    },
    {
      "Name": "Ring 0.1",
      "Identifier": "afc590da-5245-5e06-bdb7-17dd5f1bfcc6",
      "Kind": "Circle",
      "Anchor": null,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1.0,
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Offset": "0,0,0",
      "Rotation": "3.0,0,0",
      "Radius": 1.7,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": true,
      "LineStart": "0,0,0",
      "LineEnd": "0,1,0",
      "Points": [],
      "Closed": false,
      "GridCount": "5,1,5",
      "GridSpacing": "0.3,0.3,0.3",
      "Height": 2.0,
      "Turns": 3.0,
      "Count": 160
    }
  ],
  "Slots": [],
  "Anchors": [
    {
      "Name": "Planet",
      "Identifier": "7ec6601c-1f0e-58c5-be09-0ccf6d6e461b",
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1"
    },
    {
      "Name": "Io",
      "Identifier": "c9809118-89da-5c23-8c12-872ac5c159fa",
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1"
    },
    {
      "Name": "Europa",
      "Identifier": "27f59789-84c8-547b-b3a9-fe62c80bfd09",
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1"
    },
    {
      "Name": "Ganymede",
      "Identifier": "8e112876-f03d-5eca-b973-4ee6b0186435",
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1"
    },
    {
      "Name": "Callisto",
      "Identifier": "5fe9cbfb-eb8c-5206-8f46-62d42866c661",
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1"
    },
    {
      "Name": "Juno",
      "Identifier": "6b77e2e6-740c-55f5-a9ed-d2bc6be3aad9",
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1"
    }
  ],
  "FloatParameters": [
    {
      "Name": "Speed",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 3,
      "Identifier": "c5652ff3-2ee3-566a-8605-b1bee9390b2f"
    }
  ],
  "VectorParameters": [],
  "ColorParameters": [],
  "__references": [],
  "__version": 0
}