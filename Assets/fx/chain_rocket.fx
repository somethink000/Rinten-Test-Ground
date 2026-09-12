{
  "Emitters": [
    {
      "Name": "Rockets",
      "Identifier": "9eab1269-dba8-5390-bb39-ea6bc22b7ba3",
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
          "__type": "Rinten.SpawnRateModule",
          "Stage": "Spawn",
          "Rate": {
            "UseParameter": true,
            "Value": 1.2,
            "ParameterName": "Rate",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "d0003301-f1d2-5685-bfb4-5e4572177bfe",
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
          "Radius": 0.15,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "babc5860-8e7e-57bc-9a04-44c6928ee78f",
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
              "Y": 6.0,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Scatter": {
            "UseParameter": false,
            "Value": 1.6,
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
          "Identifier": "d85c6180-73fb-5577-af6c-2caf90354cb3",
          "Name": "Velocity",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 3.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "cf27a35f-7803-506f-831f-5227bbe3f74d",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": 0.06,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "2e85273b-8a24-5048-b7a8-d1a4965763e4",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": {
              "Type": "Range",
              "Evaluation": "Particle",
              "ConstantA": "1.0000,0.3137,0.3137,1.0",
              "ConstantB": "0.3137,0.6275,1.0000,1.0"
            },
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
            "Value": 2.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "62ff14ff-1465-55f5-9f59-ffb115983e27",
          "Name": "Color",
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
              "Y": -3,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Identifier": "736feda3-0ae5-5319-a0e0-f40727d75438",
          "Name": "Gravity",
          "Enabled": true
        },
        {
          "__type": "Rinten.EventModule",
          "Stage": "Update",
          "Trigger": "OnTime",
          "At": {
            "UseParameter": true,
            "Value": 1.0,
            "ParameterName": "Fuse",
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
              "Set": "LifeLeft",
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
              "Multiply": false
            }
          ],
          "Effect": "fx/chain_burst.fx",
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
          "MaxAlive": 6,
          "Context": [
            {
              "Enabled": true,
              "Source": "Color",
              "Slot": null,
              "Parameter": "Color",
              "Channel": "X",
              "Scale": 1.0,
              "FromSlot": false
            },
            {
              "Enabled": true,
              "Source": "Velocity",
              "Slot": null,
              "Parameter": "Direction",
              "Channel": "X",
              "Scale": 1.0,
              "FromSlot": false
            }
          ],
          "Identifier": "c0777216-10db-5450-af5a-cd65f3e18250",
          "Name": "Burst",
          "Enabled": true
        }
      ],
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
          "Identifier": "c40820fd-57c3-59d6-9e87-6a48633ffee9",
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
                "rangey": "0,0.03",
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
                "rangey": "0,0.03",
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
                    "c": "1.0000,1.0000,1.0000,1.0"
                  },
                  {
                    "t": 1,
                    "c": "1.0000,1.0000,1.0000,1.0"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 1.0
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
                    "c": "1.0000,1.0000,1.0000,1.0"
                  },
                  {
                    "t": 1,
                    "c": "1.0000,1.0000,1.0000,1.0"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 1.0
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
          "MaxPoints": 32,
          "PointDistance": 0.03,
          "LifeTime": 0.4,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": false,
          "TintFromParticle": true,
          "Identifier": "9f14bc32-adaf-5720-8719-b999c65bc810",
          "Name": "Trail",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 4.0,
  "Looping": true,
  "Shapes": [],
  "Slots": [],
  "Anchors": [],
  "FloatParameters": [
    {
      "Name": "Rate",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 3,
      "Identifier": "3b4cdf8f-95c4-56c2-84ad-df73bff53441"
    },
    {
      "Name": "Fuse",
      "DefaultValue": 1,
      "Min": 0.3,
      "Max": 2,
      "Identifier": "da7ac45f-21e4-5cfc-89b0-2b699b2222fd"
    }
  ],
  "VectorParameters": [],
  "ColorParameters": [],
  "__references": [],
  "__version": 0
}