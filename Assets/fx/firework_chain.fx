{
  "Emitters": [
    {
      "Name": "Rocket",
      "Identifier": "d3677176-8fb1-5af4-a0af-45e430c28fbb",
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
          "Identifier": "c7b9c163-031b-51d1-b128-962e595707d6",
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
          "Identifier": "f3ebba4a-2fbb-5cad-a44d-3af1c86ad84b",
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
                "Constants": "-1.5,1.5,0,0"
              },
              "Y": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "11,13,0,0"
              },
              "Z": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-1.5,1.5,0,0"
              }
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": "Height",
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
          "LocalSpace": false,
          "InheritEmitterVelocity": false,
          "InheritScale": 1,
          "Drift": {
            "X": 0,
            "Y": 0,
            "Z": 0
          },
          "Identifier": "34456c70-561b-58d8-9b70-02943ca204a6",
          "Name": "Velocity",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": {
              "Type": "Range",
              "Evaluation": "Seed",
              "Constants": "0.9,1.2,0,0"
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "4047306c-dd14-5d57-a53b-84717d92ed50",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.05,
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "698f39fb-be26-5bad-a6b2-3be6522bbe28",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": "1,1,1,1",
            "ParameterName": "Rocket",
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
            "Value": 2.0,
            "ParameterName": "Brightness",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "b3a01382-f75b-5732-961a-6547f21a81ee",
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
          "Identifier": "8ad72ad4-00b2-5bc1-810c-53343d4ad69d",
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
          "Identifier": "dd8658ba-c803-578a-b6b3-7dfbfaf01c94",
          "Name": "Gravity",
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
          "Identifier": "aa11adf7-a2e1-55f5-bb9d-6b3c68151c37",
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
                "rangey": "0,0.035",
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
                "rangey": "0,0.035",
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
                    "c": "1.0000,0.8471,0.6275,0.9"
                  },
                  {
                    "t": 1,
                    "c": "1.0000,0.3765,0.1255,0.0"
                  }
                ],
                "alpha": null
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "1.0000,0.8471,0.6275,0.9"
                  },
                  {
                    "t": 1,
                    "c": "1.0000,0.3765,0.1255,0.0"
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
          "MaxPoints": 40,
          "PointDistance": 0.08,
          "LifeTime": 0.6,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": false,
          "TintFromParticle": true,
          "Identifier": "c1ca3ff8-f321-5af5-9d9b-f16e9b318e8f",
          "Name": "Trail",
          "Enabled": true
        },
        {
          "__type": "Rinten.SpawnEffectOnDeathModule",
          "Stage": "Render",
          "Effect": "fx/firework_burst.fx",
          "Chance": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Scale": {
            "UseParameter": true,
            "Value": 1.0,
            "ParameterName": "Burst Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "AlignToVelocity": false,
          "OnCollision": true,
          "OnExpiry": true,
          "MaxAlive": 6,
          "Identifier": "4218fb48-4d95-5992-b1b9-72b3c218e16d",
          "Name": "Effect On Death",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "1.0000,0.7843,0.5647,1.0",
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
            "Value": 3,
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
          "Identifier": "1000ccc9-7e10-5a37-b5c3-008f14b86a4f",
          "Name": "Light",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Launch Smoke",
      "Identifier": "990086f0-900d-5df0-ac5b-a4bc92cf9b97",
      "Enabled": true,
      "MaxParticles": 30,
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
            "Value": 12,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "002ea94a-794b-5b34-b3a6-d1856bd470d8",
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
          "Identifier": "d525508b-165c-538b-9fc9-26aca74efcc1",
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
                "Constants": "-0.6,0.6,0,0"
              },
              "Y": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "0.3,1.2,0,0"
              },
              "Z": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-0.6,0.6,0,0"
              }
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
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
          "LocalSpace": false,
          "InheritEmitterVelocity": false,
          "InheritScale": 1,
          "Drift": {
            "X": 0,
            "Y": 0,
            "Z": 0
          },
          "Identifier": "3cee6d6e-d53c-511c-8d79-d2a2319c5a12",
          "Name": "Velocity",
          "Enabled": true
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
          "Identifier": "10fbeb4c-dbba-5a2c-a664-ecba912e624e",
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
                "rangey": "0,0.8",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.18749999999999997,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.8749999999999999,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,0.8",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.18749999999999997,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.8749999999999999,
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
          "Identifier": "6b7d2102-8d0f-5807-b534-75c95c0a357d",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.5412,0.5412,0.5412,1.0",
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
          "Identifier": "566178b5-3699-51e9-894d-a7d4bf18bcd8",
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
          "Identifier": "992a713f-bbfd-5ec8-91d4-08cd9314d24d",
          "Name": "Rotation",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.DragModule",
          "Stage": "Update",
          "Damping": {
            "UseParameter": false,
            "Value": 0.8,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "08ffbbe8-e2cc-5124-8cbf-3451892333c5",
          "Name": "Drag",
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
          "Identifier": "b347f0bb-9beb-5317-8842-590866857f79",
          "Name": "Sprite",
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
      "Name": "Height",
      "DefaultValue": 1,
      "Min": 0.5,
      "Max": 1.5,
      "Identifier": "4d8e20e1-713f-5f66-9118-05d33b46e38c"
    },
    {
      "Name": "Size",
      "DefaultValue": 1,
      "Min": 0.2,
      "Max": 3,
      "Identifier": "aa28643f-24dc-5d1d-8f12-1fa1d19f187c"
    },
    {
      "Name": "Brightness",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "f9173a35-a022-56bf-8bc2-6ecb19c0f068"
    },
    {
      "Name": "Burst Size",
      "DefaultValue": 1,
      "Min": 0.3,
      "Max": 3,
      "Identifier": "2f615b6d-0d80-5aa8-b06b-ea2928b08019"
    }
  ],
  "VectorParameters": [],
  "ColorParameters": [
    {
      "Name": "Rocket",
      "DefaultValue": "1.0000,0.8471,0.6275,1.0",
      "Identifier": "2ea692da-f99b-5033-880b-23428b963916"
    }
  ],
  "__references": [],
  "__version": 0
}