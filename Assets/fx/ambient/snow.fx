{
  "Emitters": [
    {
      "Name": "Flakes",
      "Identifier": "c143edff-2a77-5dbb-8e9c-6daa646d3956",
      "Enabled": true,
      "MaxParticles": 2500,
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
            "Value": 160,
            "ParameterName": "Density",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "194f7da5-c1c0-5538-bda5-45fa43cb20f7",
          "Name": "Spawn Rate",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "Shape": "Box",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "7,0.4,7",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "a50bac0b-e602-550c-b226-bca25e234bee",
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
              "Y": -0.7,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": "Fall",
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
          "Identifier": "1f2bc60d-ad42-527a-abb6-b6114c19d919",
          "Name": "Velocity",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": true,
            "Value": 8.5,
            "ParameterName": "Lifetime",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "fe597bae-e619-5ab3-97c1-6623ffee0b6a",
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
              "Constants": "0.025,0.06,0,0"
            },
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "9b9930db-123d-58cd-bc18-d109a1c00f9e",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": "1,1,1,1",
            "ParameterName": "Color",
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
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.08,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.85,
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
                  "x": 0.08,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.85,
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
            "ParameterName": "Opacity",
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
          "Identifier": "0b700d21-114f-53db-adc5-95fb25709b06",
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
          "Identifier": "b503afd7-74e5-5f5c-9b2e-dcaad60258b3",
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
                "Constants": "-70,70,0,0"
              }
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "1ce4ef6a-7e57-597b-a7b9-918a87859e5f",
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
              "Y": -1.4,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": "Fall",
            "IsBound": false
          },
          "Identifier": "c564c579-95f6-57c5-b235-ef2c2b0af802",
          "Name": "Gravity",
          "Enabled": true
        },
        {
          "__type": "Rinten.GravityModule",
          "Stage": "Update",
          "Force": {
            "UseParameter": true,
            "Value": {
              "X": 0,
              "Y": 0,
              "Z": 0
            },
            "ParameterName": "Wind",
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "a0195177-7322-5aa9-aef6-4a17490a0844",
          "Name": "Gravity",
          "Enabled": true
        },
        {
          "__type": "Rinten.DragModule",
          "Stage": "Update",
          "Damping": {
            "UseParameter": false,
            "Value": 1.6,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "03b11e40-e95e-576d-959a-225406c947cb",
          "Name": "Drag",
          "Enabled": true
        },
        {
          "__type": "Rinten.CurlNoiseModule",
          "Stage": "Update",
          "Strength": {
            "UseParameter": true,
            "Value": 0.45,
            "ParameterName": "Drift",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Scale": {
            "UseParameter": false,
            "Value": 0.8,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "TimeScale": {
            "UseParameter": false,
            "Value": 0.6,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Offset": "0,0,0",
          "Identifier": "10618358-b0af-5d44-a966-e079257f089b",
          "Name": "Curl Noise",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/flake.sprite",
          "Scale": 1.0,
          "Alignment": "LookAtCamera",
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
          "Identifier": "a250e7f0-fa3c-5a7d-a668-604bcdaddc19",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Haze",
      "Identifier": "05bceba5-868e-5c26-bef4-e6fabf3f1d8b",
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
            "UseParameter": true,
            "Value": 6,
            "ParameterName": "Haze",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "355b8fb1-a653-5667-8b62-3109f6f4fc5a",
          "Name": "Spawn Rate",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "Shape": "Box",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "7,0.2,7",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "a2005bbf-35ac-538e-8950-b2331cb805a4",
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
              "Y": -0.3,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": "Fall",
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
          "Identifier": "b339af8b-259e-5010-a68f-b65a6b6b9e17",
          "Name": "Velocity",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": true,
            "Value": 7,
            "ParameterName": "Lifetime",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "41531a01-afd8-5bc5-88e6-9780d01681c9",
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
                "rangey": "0,2",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.4,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.8,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,2",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.4,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.8,
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
          "Identifier": "0ce544c6-4fca-5609-8362-8142b07916b3",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.8745,0.9098,0.9608,1.0",
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
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.2,
                  "y": 0.08,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.8,
                  "y": 0.08,
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
                  "y": 0.08,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.8,
                  "y": 0.08,
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
            "ParameterName": "Opacity",
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
          "Identifier": "9c88c305-647c-50d1-8498-86dbdfaf56da",
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
          "Identifier": "d0426db7-7f86-573e-b198-2f08c30a7507",
          "Name": "Rotation",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.GravityModule",
          "Stage": "Update",
          "Force": {
            "UseParameter": true,
            "Value": {
              "X": 0,
              "Y": 0,
              "Z": 0
            },
            "ParameterName": "Wind",
            "Multiplier": 0.6,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "7ee61508-1769-5c0b-8e03-365ca4170e7c",
          "Name": "Gravity",
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
          "Identifier": "bc06a301-6770-51c0-8917-30cdc3b8a7eb",
          "Name": "Drag",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/smoke2.sprite",
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
          "Identifier": "11fc16d5-54d1-5e17-bb13-ee0ff63c851f",
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
      "Name": "Density",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "53b1d8e8-cb8d-5063-800f-8e438bbd0290"
    },
    {
      "Name": "Fall",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "ffe76163-2b06-524d-9dcd-6fbef45b03a7"
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
      "Max": 2,
      "Identifier": "217a743c-8b19-5549-aa37-f2d90240fd19"
    },
    {
      "Name": "Drift",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "5de035f2-ecc9-59a9-a2a1-4c6fac05b607"
    },
    {
      "Name": "Opacity",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 1,
      "Identifier": "7ea504c9-b123-54f7-a690-4c3ce1eb89d5"
    },
    {
      "Name": "Haze",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "e544373e-694f-5ac2-aa92-c78e49d7cd4a"
    }
  ],
  "VectorParameters": [
    {
      "Name": "Wind",
      "DefaultValue": "0.7,0,0",
      "Identifier": "6b3a4e9e-f658-5b5d-871d-0e7cfa79ee0a"
    }
  ],
  "ColorParameters": [
    {
      "Name": "Color",
      "DefaultValue": "1.0000,1.0000,1.0000,1.0",
      "Identifier": "93376221-c204-5096-811a-4e459dc336c9"
    }
  ],
  "__references": [],
  "__version": 0
}