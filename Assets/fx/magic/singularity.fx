{
  "Emitters": [
    {
      "Name": "Core",
      "Identifier": "78ebc238-b554-5b41-b4f4-bf493c14935d",
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
          "__type": "Rinten.SpawnRateModule",
          "Stage": "Spawn",
          "Rate": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "56eff625-2837-5772-acf0-b035cfb7675b",
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
          "Identifier": "dc5cff85-de2d-500d-9bed-58257f7ec5f2",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 1.2,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "e9a2da53-83de-5ef9-b6dc-1b467e8a2939",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.35,
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "ee8e3ed9-f0ab-5498-95e4-90cacf26a614",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.0627,0.0314,0.0941,1.0",
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
          "Identifier": "03173510-cdfa-50f1-a3fe-b7a58c6fa4a0",
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
          "Identifier": "ef3a4d3e-1fc4-5c7c-91a6-b9fb9f8791b3",
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
              "X": 0,
              "Y": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "60,120,0,0"
              },
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "58d228ee-5cf4-57ba-b94a-7374ea68bd95",
          "Name": "Spin",
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
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "RotateWithObject": false,
          "CastShadows": false,
          "Identifier": "0bec0057-4e2e-58bf-94df-89ff413d6a29",
          "Name": "Model",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Halo",
      "Identifier": "3715853d-52f0-5a5d-a35b-22c5fdf3a7f3",
      "Enabled": true,
      "MaxParticles": 12,
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
            "Value": 4,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "661622f6-7825-504b-8314-de3e89806d96",
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
          "Identifier": "c9a6059a-9c74-5cc7-b728-f4a591ba4f04",
          "Name": "Position",
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
          "Identifier": "b36c4ff3-125b-5b10-9406-f3d5ccd5aee5",
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
                "rangey": "0,1.2",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.5833333333333334,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.9166666666666667,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,1.2",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.5833333333333334,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.9166666666666667,
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
          "Identifier": "6e807581-82f6-5882-9443-2e3501a798c6",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": "1,1,1,1",
            "ParameterName": "Halo",
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
                  "x": 0.4,
                  "y": 0.5,
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
                  "x": 0.4,
                  "y": 0.5,
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
            "Value": 1.3,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "c701a2df-f3b9-5f6d-ad3c-a7b75c94ca0b",
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
          "Identifier": "356916da-6dea-5733-a8cf-f9c64da84d21",
          "Name": "Sprite",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "0.6275,0.3765,1.0000,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": true,
            "Value": 8,
            "ParameterName": "Glow",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Radius": {
            "UseParameter": false,
            "Value": 6,
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
            "Value": 0.5,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "UseParticleColor": false,
          "CastShadows": false,
          "Identifier": "df9105cc-dab5-5a85-b4c2-88206966d639",
          "Name": "Light",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Infall",
      "Identifier": "1acf1542-0d95-5f4d-965c-7be52ff87b5f",
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
          "__type": "Rinten.SpawnRateModule",
          "Stage": "Spawn",
          "Rate": {
            "UseParameter": true,
            "Value": 30,
            "ParameterName": "Density",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "f6df6673-548f-5eb3-9dc4-82d17088d22c",
          "Name": "Spawn Rate",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "Shape": "Sphere",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 3.0,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": true,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "a067c008-46cd-559e-97dc-592ea514b2fe",
          "Name": "Position",
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
              "Constants": "2.0,3.0,0,0"
            },
            "ParameterName": "Lifetime",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "17fa1e5a-d034-5e0b-9c88-772d3508451e",
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
              "Constants": "0.02,0.05,0,0"
            },
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "ce39aafd-d56c-573c-bd11-0c326ab97570",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": "1,1,1,1",
            "ParameterName": "Streaks",
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
                  "x": 0.15,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.9,
                  "y": 1.0,
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
                  "x": 0.15,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.9,
                  "y": 1.0,
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
            "UseParameter": true,
            "Value": 1.5,
            "ParameterName": "Brightness",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "1347245d-db7b-5519-b7ca-2d88f4ca423e",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.OrbitModule",
          "Stage": "Update",
          "Space": "Local",
          "Center": "0,0,0",
          "Axis": {
            "UseParameter": false,
            "Value": {
              "X": 0,
              "Y": 1,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Speed": {
            "UseParameter": true,
            "Value": 90,
            "ParameterName": "Spin",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "67be8bd3-25c0-5dba-9d0b-2d43846231d0",
          "Name": "Orbit",
          "Enabled": true
        },
        {
          "__type": "Rinten.AttractorModule",
          "Stage": "Update",
          "Space": "Local",
          "Position": {
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
          "Strength": {
            "UseParameter": true,
            "Value": 2.5,
            "ParameterName": "Pull",
            "Mode": "Multiply",
            "Multiplier": 2.5,
            "IsBound": false
          },
          "Size": 0.35,
          "Invert": false,
          "Falloff": 0.6,
          "Identifier": "3b2da11d-053b-5623-8c66-22c03f05e4eb",
          "Name": "Attractor",
          "Enabled": true
        },
        {
          "__type": "Rinten.DragModule",
          "Stage": "Update",
          "Damping": {
            "UseParameter": false,
            "Value": 0.2,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "a31716a3-4e20-5706-9749-ce2a39469e3c",
          "Name": "Drag",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/spark.sprite",
          "Scale": 1.0,
          "Alignment": "LookAtCamera",
          "FaceVelocity": true,
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
          "Identifier": "805a6af4-5105-52a7-ae0f-2d1659f5cc2a",
          "Name": "Sprite",
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
                "rangey": "0,0.02",
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
                "rangey": "0,0.02",
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
                    "c": "0.7529,0.6275,1.0000,0.6"
                  },
                  {
                    "t": 1,
                    "c": "0.2510,0.1255,0.6275,0.0"
                  }
                ],
                "alpha": null
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "0.7529,0.6275,1.0000,0.6"
                  },
                  {
                    "t": 1,
                    "c": "0.2510,0.1255,0.6275,0.0"
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
          "MaxPoints": 36,
          "PointDistance": 0.035,
          "LifeTime": 0.4,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": false,
          "TintFromParticle": true,
          "Identifier": "cfd2126a-7f7f-5436-b6e8-45d0d268918e",
          "Name": "Trail",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Disc",
      "Identifier": "bbbea85d-c207-5fa1-aa66-a9bb6fae298a",
      "Enabled": true,
      "MaxParticles": 500,
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
            "UseParameter": true,
            "Value": 120,
            "ParameterName": "Density",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "ab2ea98c-d171-556c-bf44-4c9bb1fd092d",
          "Name": "Spawn Rate",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "Shape": "Circle",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 1.8,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": true,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "24760330-0933-585f-b35c-7d3f6f991901",
          "Name": "Position",
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
              "Constants": "1.5,2.5,0,0"
            },
            "ParameterName": "Lifetime",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "ec94b367-d5d1-55e5-81ee-5abc6d02fe19",
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
              "Constants": "0.015,0.03,0,0"
            },
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "ea9a8a1e-82dd-5d03-8833-2e1ccc110fdd",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": "1,1,1,1",
            "ParameterName": "Disc",
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
                  "x": 0.2,
                  "y": 0.8,
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
                  "x": 0.2,
                  "y": 0.8,
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
            "UseParameter": true,
            "Value": 1.3,
            "ParameterName": "Brightness",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "2244cbf6-b1cc-5a76-92e4-31de4ebd440a",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.OrbitModule",
          "Stage": "Update",
          "Space": "Local",
          "Center": "0,0,0",
          "Axis": {
            "UseParameter": false,
            "Value": {
              "X": 0,
              "Y": 1,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Speed": {
            "UseParameter": true,
            "Value": 220,
            "ParameterName": "Spin",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "a9fe1aff-0986-5a1c-9cdc-6e1e049e1364",
          "Name": "Orbit",
          "Enabled": true
        },
        {
          "__type": "Rinten.AttractorModule",
          "Stage": "Update",
          "Space": "Local",
          "Position": {
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
          "Strength": {
            "UseParameter": true,
            "Value": 0.8,
            "ParameterName": "Pull",
            "Mode": "Multiply",
            "Multiplier": 0.8,
            "IsBound": false
          },
          "Size": 0.35,
          "Invert": false,
          "Falloff": 0.6,
          "Identifier": "39f2dd30-768d-5323-89e7-3e16e9e39ebb",
          "Name": "Attractor",
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
          "Identifier": "2d348ff5-1312-57f7-a3ac-b461221c2cc4",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 6,
  "Looping": true,
  "Shapes": [],
  "Slots": [],
  "Anchors": [],
  "FloatParameters": [
    {
      "Name": "Spin",
      "DefaultValue": 1,
      "Min": -3,
      "Max": 3,
      "Identifier": "88565ac8-e6a8-5c18-9984-ca2f7499ee8a"
    },
    {
      "Name": "Pull",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "e4cd8c26-2658-5cb4-af6b-33990acfb097"
    },
    {
      "Name": "Density",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "53b1d8e8-cb8d-5063-800f-8e438bbd0290"
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
      "Name": "Brightness",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "f9173a35-a022-56bf-8bc2-6ecb19c0f068"
    },
    {
      "Name": "Glow",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "6e941755-ba13-5f6b-b668-a3913c5a96a2"
    }
  ],
  "VectorParameters": [],
  "ColorParameters": [
    {
      "Name": "Halo",
      "DefaultValue": "0.5020,0.2510,1.0000,1.0",
      "Identifier": "d3dfe2df-3174-5f98-9135-40c584d9645c"
    },
    {
      "Name": "Streaks",
      "DefaultValue": {
        "Type": "Gradient",
        "Evaluation": "Life",
        "GradientA": {
          "blend": "Linear",
          "color": [
            {
              "t": 0,
              "c": "1.0000,1.0000,1.0000,1.0"
            },
            {
              "t": 1,
              "c": "0.6275,0.3765,1.0000,1.0"
            }
          ],
          "alpha": null
        },
        "GradientB": {
          "blend": "Linear",
          "color": [
            {
              "t": 0,
              "c": "1.0000,1.0000,1.0000,1.0"
            },
            {
              "t": 1,
              "c": "0.6275,0.3765,1.0000,1.0"
            }
          ],
          "alpha": null
        }
      },
      "Identifier": "cba8a5bc-7709-5142-a68d-9e8b4fb53d10"
    },
    {
      "Name": "Disc",
      "DefaultValue": {
        "Type": "Gradient",
        "Evaluation": "Life",
        "GradientA": {
          "blend": "Linear",
          "color": [
            {
              "t": 0,
              "c": "1.0000,0.8784,0.7529,1.0"
            },
            {
              "t": 1,
              "c": "1.0000,0.3765,0.6275,1.0"
            }
          ],
          "alpha": null
        },
        "GradientB": {
          "blend": "Linear",
          "color": [
            {
              "t": 0,
              "c": "1.0000,0.8784,0.7529,1.0"
            },
            {
              "t": 1,
              "c": "1.0000,0.3765,0.6275,1.0"
            }
          ],
          "alpha": null
        }
      },
      "Identifier": "b4cf4a11-0736-5d4b-b1dd-0f584b34f19c"
    }
  ],
  "__references": [],
  "__version": 0
}