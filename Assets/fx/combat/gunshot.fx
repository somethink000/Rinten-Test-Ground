{
  "Emitters": [
    {
      "Name": "Flash",
      "Identifier": "5f7df139-2080-5318-ba06-db00f8c4eb2f",
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
          "Identifier": "2411bb8c-a543-5c86-a481-87c5a22de9f9",
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
          "Identifier": "014242f0-0574-5997-ba9d-37ce12895c50",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": true,
            "Value": 0.07,
            "ParameterName": "Lifetime",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "c5be951c-afa2-53e6-8acc-833b432f0c7e",
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
              "Constants": "0.55,0.85,0,0"
            },
            "ParameterName": "Flash Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "71b2c7bd-5eca-546a-8b4e-dfd68a49030e",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": "1,1,1,1",
            "ParameterName": "Flash",
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
              ],
              "CurveB": [
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
          "Identifier": "a1406c59-014f-57d0-b9f0-0eb028ae1a48",
          "Name": "Color",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeRotationModule",
          "Stage": "Initialize",
          "Rotation": {
            "X": 0,
            "Y": 0,
            "Z": {
              "Type": "Range",
              "Evaluation": "Seed",
              "Constants": "0,360,0,0"
            }
          },
          "Identifier": "4b95f2e4-81b4-59dd-92e1-bedd581094a6",
          "Name": "Rotation",
          "Enabled": true
        }
      ],
      "UpdateModules": [],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/flash.sprite",
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
          "Identifier": "1dde33ce-bcac-52f1-aa4f-5e8d7ac6acc5",
          "Name": "Sprite",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "1.0000,0.7529,0.4392,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": true,
            "Value": 12,
            "ParameterName": "Glow",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Radius": {
            "UseParameter": false,
            "Value": 4,
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
          "Identifier": "0c10fb25-65b3-5cfc-a5e9-248485a99940",
          "Name": "Light",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Core",
      "Identifier": "4c488098-696a-5b9a-b729-a1ad9414e3a1",
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
          "Identifier": "f0851e48-1f2b-586e-bcdc-4c23dbe2185d",
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
          "Identifier": "0dd707d3-e6ac-513f-ade0-e2b0a38c82c5",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": true,
            "Value": 0.09,
            "ParameterName": "Lifetime",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "79e4cf4b-7407-524f-bfff-60b994665e01",
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
                "rangey": "0,0.7",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.5,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.8571428571428572,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,0.7",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.5,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.8571428571428572,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              }
            },
            "ParameterName": "Flash Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "5fcbcd34-85ee-53d0-bc6d-dfde2b0939ae",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "1.0000,0.7216,0.4706,1.0",
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
            "UseParameter": true,
            "Value": 1.2,
            "ParameterName": "Brightness",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "884ffe4b-f94c-5c53-8de9-5aece4b71bc2",
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
          "Identifier": "cb16e786-8fb6-5ad2-aacd-2ac6e8266394",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Sparks",
      "Identifier": "31e1ac64-a3b4-5837-856e-32818e6029f4",
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
          "__type": "Rinten.SpawnBurstModule",
          "Stage": "Spawn",
          "Count": {
            "UseParameter": true,
            "Value": 14,
            "ParameterName": "Sparks",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "0c14d9b5-d461-5b0a-b514-056fde5448f7",
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
          "Identifier": "7d8a749f-97ef-5978-ad37-031e848ee3ea",
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
              "Y": 0,
              "Z": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-13,-22,0,0"
              }
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": "Speed",
            "IsBound": false
          },
          "Scatter": {
            "UseParameter": true,
            "Value": 2.5,
            "ParameterName": "Spread",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "LocalSpace": true,
          "InheritEmitterVelocity": false,
          "InheritScale": 1,
          "Drift": {
            "X": 0,
            "Y": 0,
            "Z": 0
          },
          "Identifier": "1f856d8d-757d-506f-8587-3875bbf785cc",
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
              "Constants": "0.15,0.32,0,0"
            },
            "ParameterName": "Lifetime",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "4cf380c2-bc81-5b74-a805-ac3ae58e1455",
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
              "Constants": "0.02,0.035,0,0"
            },
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "5c292b4c-b501-5e6a-aaf1-9cc9252b4a29",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "1.0000,0.8784,0.6275,1.0",
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
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.6,
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
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.6,
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
          "Identifier": "d2ba936c-067a-545a-9516-9782fa8276d5",
          "Name": "Color",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeStretchModule",
          "Stage": "Initialize",
          "Stretch": {
            "UseParameter": false,
            "Value": 4,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "20171a33-9e61-50b6-bf5e-95617c349392",
          "Name": "Stretch",
          "Enabled": true
        }
      ],
      "UpdateModules": [
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
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "5ca74b17-cb22-5b2a-92e0-43dec23513ee",
          "Name": "Gravity",
          "Enabled": true
        },
        {
          "__type": "Rinten.DragModule",
          "Stage": "Update",
          "Damping": {
            "UseParameter": false,
            "Value": 1.5,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "8bda17e5-1c8d-5fbb-8c02-e62c89636921",
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
          "MotionBlur": true,
          "LeadingTrail": true,
          "BlurAmount": 0.6,
          "BlurSpacing": 0.3,
          "BlurOpacity": 0.5,
          "Identifier": "13c9b38d-1a7e-516c-aff9-b3593e280ae9",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Smoke",
      "Identifier": "b5f34c47-58a4-589f-ab09-6ad9e6ca369f",
      "Enabled": true,
      "MaxParticles": 40,
      "Places": 0,
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1",
      "Anchor": null,
      "Delay": 0.02,
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
            "Value": 9,
            "ParameterName": "Smoke",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "845c8b3e-d6cd-5829-94d5-907837ae2e11",
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
          "Identifier": "6dc28228-dad2-547a-9ddd-6ee35d7cfc94",
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
                "Constants": "-0.5,0.5,0,0"
              },
              "Y": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "0.4,1.0,0,0"
              },
              "Z": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-2.5,-4.5,0,0"
              }
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": "Speed",
            "IsBound": false
          },
          "Scatter": {
            "UseParameter": true,
            "Value": 0.4,
            "ParameterName": "Spread",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "LocalSpace": true,
          "InheritEmitterVelocity": false,
          "InheritScale": 1,
          "Drift": {
            "X": 0,
            "Y": 0,
            "Z": 0
          },
          "Identifier": "8578ac67-5510-576b-a081-a1c41630aebf",
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
              "Constants": "0.7,1.3,0,0"
            },
            "ParameterName": "Lifetime",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "82b38261-d3ae-5a5b-8bb3-e4e2ac70bab0",
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
                "rangey": "0,0.7",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.17142857142857143,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.8571428571428572,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,0.7",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.17142857142857143,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.8571428571428572,
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
          "Identifier": "fdf3aaba-44cc-5fcd-96ee-9922c2e6e86c",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.6039,0.6039,0.6039,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": true,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": [
                {
                  "x": 0,
                  "y": 0.4,
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
                  "y": 0.4,
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
            "ParameterName": "Smoke Opacity",
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
          "Identifier": "66a963e4-0518-5fcf-971d-c480a722d96d",
          "Name": "Color",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeRotationModule",
          "Stage": "Initialize",
          "Rotation": {
            "X": 0,
            "Y": 0,
            "Z": {
              "Type": "Range",
              "Evaluation": "Seed",
              "Constants": "0,360,0,0"
            }
          },
          "Identifier": "b3eb1bbe-8f36-5455-b587-872c92c1153b",
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
              "Y": 0,
              "Z": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-40,40,0,0"
              }
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "ca6d0e13-e9ad-5a9a-b3f2-0f01b8041a5d",
          "Name": "Spin",
          "Enabled": true
        },
        {
          "__type": "Rinten.DragModule",
          "Stage": "Update",
          "Damping": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "3cc776e7-76cb-576f-9b41-a029dfe0a0a1",
          "Name": "Drag",
          "Enabled": true
        },
        {
          "__type": "Rinten.GravityModule",
          "Stage": "Update",
          "Force": {
            "UseParameter": false,
            "Value": {
              "X": 0,
              "Y": 0.5,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "57fabb73-035e-5fa2-9ad7-c7398b1edb47",
          "Name": "Gravity",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/smoke4.sprite",
          "Scale": 1.0,
          "Alignment": "LookAtCamera",
          "FaceVelocity": false,
          "Additive": false,
          "Shadows": false,
          "Lighting": true,
          "DepthFeather": 0,
          "SortMode": "ByDistance",
          "Opaque": false,
          "FogStrength": 1.0,
          "TextureFilter": "Bilinear",
          "MotionBlur": false,
          "LeadingTrail": true,
          "BlurAmount": 0.5,
          "BlurSpacing": 0.5,
          "BlurOpacity": 0.5,
          "Identifier": "f24aacd9-c546-5e4b-8adc-2c0b8f6057cf",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Tracer",
      "Identifier": "920e8792-531c-54c5-b05e-96c0a3bbfc86",
      "Enabled": true,
      "MaxParticles": 8,
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
          "Identifier": "06c864ad-85b3-5e56-affe-e8e7ac297a26",
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
          "Identifier": "d978c1d3-468f-5e5f-a918-3de43a0f9ba0",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeVelocityModule",
          "Stage": "Initialize",
          "Velocity": {
            "UseParameter": true,
            "Value": {
              "X": 0,
              "Y": 0,
              "Z": -40
            },
            "ParameterName": "Tracer",
            "Multiplier": 1.0,
            "ScaleParameterName": "Speed",
            "IsBound": false
          },
          "Scatter": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "LocalSpace": true,
          "InheritEmitterVelocity": false,
          "InheritScale": 1,
          "Drift": {
            "X": 0,
            "Y": 0,
            "Z": 0
          },
          "Identifier": "1e4e240e-9f33-51b7-92cf-356e861b2037",
          "Name": "Velocity",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 0.7,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "530689a4-cb34-57ac-856c-fe05e053dac0",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.045,
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "33ada700-652d-5d92-baab-04de9eec910f",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": "1,1,1,1",
            "ParameterName": "Tracer Color",
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
            "UseParameter": true,
            "Value": 2,
            "ParameterName": "Brightness",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "f35ac6e2-5c1e-5b28-861b-8544ed5074eb",
          "Name": "Color",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeStretchModule",
          "Stage": "Initialize",
          "Stretch": {
            "UseParameter": false,
            "Value": 14,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "ba146415-539c-5a8e-a8a2-bc7d8b46009c",
          "Name": "Stretch",
          "Enabled": true
        }
      ],
      "UpdateModules": [],
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
          "MotionBlur": true,
          "LeadingTrail": true,
          "BlurAmount": 1.0,
          "BlurSpacing": 0.5,
          "BlurOpacity": 0.6,
          "Identifier": "14e310dd-d109-5caa-ba1d-bb68cb0f0143",
          "Name": "Sprite",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "1.0000,0.8157,0.5020,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 3,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Radius": {
            "UseParameter": false,
            "Value": 2,
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
          "Identifier": "710e1de0-e7bd-5a84-891a-79513c0ea4a6",
          "Name": "Light",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Casing",
      "Identifier": "e0b0db64-1b0a-57d2-a9fd-ae5d33377a0a",
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
          "Identifier": "231945db-59e1-57c9-a157-a670556fa536",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "Shape": "Point",
          "Offset": "0.08,-0.02,0.15",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "c84e591f-6505-59ff-9940-416e3df56a01",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeVelocityModule",
          "Stage": "Initialize",
          "Velocity": {
            "UseParameter": false,
            "Value": {
              "X": 2.2,
              "Y": 1.6,
              "Z": 0.3
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Scatter": {
            "UseParameter": false,
            "Value": 0.4,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "LocalSpace": true,
          "InheritEmitterVelocity": false,
          "InheritScale": 1,
          "Drift": {
            "X": 0,
            "Y": 0,
            "Z": 0
          },
          "Identifier": "2873660a-0495-594c-84a0-16003d93d998",
          "Name": "Velocity",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 2.5,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "a9256fff-0780-5c11-b753-3392c3016618",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": 0.018,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "5dd3ca59-f3e4-5f5c-9f91-9a224cf95f2f",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.8471,0.6902,0.3765,1.0",
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
          "Identifier": "dba64dac-5e41-587d-b43e-3fb93d04af6d",
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
          "Identifier": "97d120c6-1d8c-5f63-84e1-b35a95cef427",
          "Name": "Rotation",
          "Enabled": true
        },
        {
          "__type": "Rinten.ParticleCollisionModule",
          "Stage": "Initialize",
          "Ignore": "",
          "Radius": {
            "UseParameter": false,
            "Value": 0.01,
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
            "Value": 0.45,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Friction": {
            "UseParameter": false,
            "Value": 0.7,
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
          "Identifier": "48a877f9-a482-5e49-9de5-0f5939bc5b4b",
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
          "Identifier": "3383d712-ceaf-553e-ba02-c65a21eba4e7",
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
                  "X": 0.2,
                  "Y": 0.2,
                  "Z": 0.2
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
          "Identifier": "cf6dd8c2-e82a-5aaf-b5d9-a4085ee72767",
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
                "Constants": "-900,900,0,0"
              },
              "Y": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-900,900,0,0"
              },
              "Z": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-900,900,0,0"
              }
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false,
            "SlotName": "Spin",
            "SlotMode": "Multiply"
          },
          "Identifier": "df4afce1-271a-5d26-9d9d-9b759e27a409",
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
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "1433fc60-fb14-5052-97f3-67ac22e3c548",
          "Name": "Gravity",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/box.mdl",
          "Material": "materials/fx/stylized_white.mat",
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
              "Name": "Edge",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.05,
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
                "UseParameter": false,
                "Value": 0.8,
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
              "Name": "Scroll",
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
          "ParticleAttributes": true,
          "Identifier": "208188e6-832c-5b27-ba37-8dd19b55aea1",
          "Name": "Mesh",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 0.42,
  "Looping": true,
  "Shapes": [],
  "Slots": [
    "Spin"
  ],
  "Anchors": [],
  "FloatParameters": [
    {
      "Name": "Spread",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "7c0de9d5-fe66-5241-a9cb-02e6765613d0"
    },
    {
      "Name": "Speed",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "c5652ff3-2ee3-566a-8605-b1bee9390b2f"
    },
    {
      "Name": "Flash Size",
      "DefaultValue": 1,
      "Min": 0.2,
      "Max": 3,
      "Identifier": "ef236dea-68fc-550b-a532-5b9e8111b047"
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
      "Name": "Sparks",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "a4d58712-e497-53fa-8bd3-341d4ac69130"
    },
    {
      "Name": "Smoke",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "addc6862-f8a4-50dd-92bb-68718da2752a"
    },
    {
      "Name": "Smoke Opacity",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 2,
      "Identifier": "a91a421c-1e05-538c-89bc-764509016529"
    },
    {
      "Name": "Glow",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "6e941755-ba13-5f6b-b668-a3913c5a96a2"
    }
  ],
  "VectorParameters": [
    {
      "Name": "Tracer",
      "DefaultValue": "0,0,-40",
      "Identifier": "10f55e41-8b6b-5a93-9ae7-c71379e91ab6"
    }
  ],
  "ColorParameters": [
    {
      "Name": "Flash",
      "DefaultValue": "1.0000,0.8510,0.6275,1.0",
      "Identifier": "6c63ca97-0a40-54e7-9a74-9b1790172589"
    },
    {
      "Name": "Tracer Color",
      "DefaultValue": "1.0000,0.9098,0.7216,1.0",
      "Identifier": "9a637e88-0c8f-5dad-a1e3-3c0a4224da1b"
    }
  ],
  "__references": [],
  "__version": 0
}