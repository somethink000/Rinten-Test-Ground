{
  "Emitters": [
    {
      "Name": "Runes",
      "Identifier": "52797e58-bab1-5037-9428-453d15928728",
      "Enabled": true,
      "MaxParticles": 8,
      "Places": 8,
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
            "Value": 8,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "16f0e4cc-65ad-5984-bc68-28b419bab31f",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": "Ring",
          "Sample": "ByIndex",
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
          "Shape": "Point",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "aa1deed9-25cd-5120-9349-cadbc0b94476",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 10000,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "3a575eb3-3fef-5255-8301-4ad4e57a6d0f",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.14,
            "ParameterName": "Size",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "InheritEmitterScale": true,
          "Identifier": "ca7161e4-a8b5-5b3a-be0c-090f80438d20",
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
              "Evaluation": "Index",
              "GradientA": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "1,0.902,0.502,1"
                  },
                  {
                    "t": 0.5,
                    "c": "1,1,1,1"
                  },
                  {
                    "t": 1,
                    "c": "1,0.902,0.502,1"
                  }
                ],
                "alpha": null
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "1,0.902,0.502,1"
                  },
                  {
                    "t": 0.5,
                    "c": "1,1,1,1"
                  },
                  {
                    "t": 1,
                    "c": "1,0.902,0.502,1"
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
            "Value": 1.8,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "e33e498a-14cb-5bab-8e18-e3b6ea19fec3",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Ring",
          "Sample": "ByIndex",
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
          "Stagger": {
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
          "Speed": {
            "UseParameter": true,
            "Value": 0.12,
            "ParameterName": "Spin",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Loop": true,
          "Weight": {
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
          "AlignToShape": false,
          "Identifier": "b802eb4d-0c0b-5e3a-bf42-fd39d6ca1cbf",
          "Name": "Turn The Ring",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/ring.sprite",
          "Scale": 1,
          "Alignment": "LookAtCamera",
          "FaceVelocity": false,
          "Additive": true,
          "Shadows": false,
          "Lighting": false,
          "DepthFeather": 0,
          "SortMode": "Unsorted",
          "Opaque": false,
          "FogStrength": 1,
          "TextureFilter": "Bilinear",
          "MotionBlur": false,
          "LeadingTrail": true,
          "BlurAmount": 0.5,
          "BlurSpacing": 0.5,
          "BlurOpacity": 0.5,
          "Identifier": "e68d363d-6588-5616-a496-54bf63e59fc0",
          "Name": "Sprite",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "1,0.8157,0.3765,1",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 1.5,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Radius": {
            "UseParameter": false,
            "Value": 1.2,
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
            "Value": 8,
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
          "UseParticleColor": true,
          "CastShadows": false,
          "Identifier": "90b4c3f3-05ac-51ed-838f-a8bb59bcf6f7",
          "Name": "Light",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Streamers",
      "Identifier": "d9239b8c-102e-527f-a9c6-e2d1f97121d2",
      "Enabled": true,
      "MaxParticles": 60,
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
          "__type": "Rinten.SpawnRateModule",
          "Stage": "Spawn",
          "Rate": {
            "UseParameter": true,
            "Value": 10,
            "ParameterName": "Intensity",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Identifier": "72e0814f-3551-5998-a3ea-81115c336c10",
          "Name": "Spawn Rate",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": "Helix",
          "Sample": "ByTime",
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
          "Shape": "Point",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "ce8d06af-b5c9-5e63-be84-a616d5db27d1",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 1.8,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "7921d794-ffc0-58d6-8557-e42096b685cc",
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
                "rangey": "0,0.100000001",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.2,
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
                    "y": 0,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,0.100000001",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.2,
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
                    "y": 0,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              }
            },
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "540e6761-1f2b-58ac-8c31-bd7dc2d10308",
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
                    "c": "0.502,1,0.6902,1"
                  },
                  {
                    "t": 0.6,
                    "c": "0.251,0.8784,1,1"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,1"
                  }
                ],
                "alpha": null
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "0.502,1,0.6902,1"
                  },
                  {
                    "t": 0.6,
                    "c": "0.251,0.8784,1,1"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,1"
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
            "Value": 2,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "3b0d9cd5-47c7-59ed-8751-981b630230a4",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Helix",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": true,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": [
                {
                  "x": 0,
                  "y": 0,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                },
                {
                  "x": 1,
                  "y": 1,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                }
              ],
              "CurveB": [
                {
                  "x": 0,
                  "y": 0,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                },
                {
                  "x": 1,
                  "y": 1,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                }
              ]
            },
            "ParameterName": "Rise",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Stagger": {
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
          "Speed": {
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
          "Loop": false,
          "Weight": {
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
          "AlignToShape": true,
          "Identifier": "26902e6e-4513-56b9-9ccc-4cec898a6dcf",
          "Name": "Follow Shape",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/glow.sprite",
          "Scale": 1,
          "Alignment": "LookAtCamera",
          "FaceVelocity": false,
          "Additive": true,
          "Shadows": false,
          "Lighting": false,
          "DepthFeather": 0,
          "SortMode": "Unsorted",
          "Opaque": false,
          "FogStrength": 1,
          "TextureFilter": "Bilinear",
          "MotionBlur": false,
          "LeadingTrail": true,
          "BlurAmount": 0.5,
          "BlurSpacing": 0.5,
          "BlurOpacity": 0.5,
          "Identifier": "818d1c9b-6cd4-5188-a9e6-457a6ffd8a02",
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
                "rangey": "0,0.0500000007",
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
                "rangey": "0,0.0500000007",
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
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
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
                    "c": "0.3765,1,0.7529,1"
                  },
                  {
                    "t": 1,
                    "c": "0.3765,1,0.7529,1"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 1
                  },
                  {
                    "t": 1,
                    "a": 0
                  }
                ]
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "0.3765,1,0.7529,1"
                  },
                  {
                    "t": 1,
                    "c": "0.3765,1,0.7529,1"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 1
                  },
                  {
                    "t": 1,
                    "a": 0
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
          "PointDistance": 0.04,
          "LifeTime": 0.6,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": true,
          "TintFromParticle": true,
          "Identifier": "2eee550d-a1ad-5525-91ff-105407c99282",
          "Name": "Trail",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Streamers Copy",
      "Identifier": "5d77b29c-4fde-4e45-8e9d-1ca3252a7f93",
      "Enabled": true,
      "MaxParticles": 60,
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
          "__type": "Rinten.SpawnRateModule",
          "Stage": "Spawn",
          "Rate": {
            "UseParameter": true,
            "Value": 10,
            "ParameterName": "Intensity",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Identifier": "72e0814f-3551-5998-a3ea-81115c336c10",
          "Name": "Spawn Rate",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": "Helix",
          "Sample": "ByTime",
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
          "Shape": "Point",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "ce8d06af-b5c9-5e63-be84-a616d5db27d1",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 1.8,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "7921d794-ffc0-58d6-8557-e42096b685cc",
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
                "rangey": "0,0.100000001",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.2,
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
                    "y": 0,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,0.100000001",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.2,
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
                    "y": 0,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              }
            },
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "540e6761-1f2b-58ac-8c31-bd7dc2d10308",
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
                    "c": "0.502,1,0.6902,1"
                  },
                  {
                    "t": 0.6,
                    "c": "0.251,0.8784,1,1"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,1"
                  }
                ],
                "alpha": null
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "0.502,1,0.6902,1"
                  },
                  {
                    "t": 0.6,
                    "c": "0.251,0.8784,1,1"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,1"
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
            "Value": 2,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "3b0d9cd5-47c7-59ed-8751-981b630230a4",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Helix 2",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": true,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": [
                {
                  "x": 0,
                  "y": 0,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                },
                {
                  "x": 1,
                  "y": 1,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                }
              ],
              "CurveB": [
                {
                  "x": 0,
                  "y": 0,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                },
                {
                  "x": 1,
                  "y": 1,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                }
              ]
            },
            "ParameterName": "Rise",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Stagger": {
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
          "Speed": {
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
          "Loop": false,
          "Weight": {
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
          "AlignToShape": true,
          "Identifier": "26902e6e-4513-56b9-9ccc-4cec898a6dcf",
          "Name": "Follow Shape",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/glow.sprite",
          "Scale": 1,
          "Alignment": "LookAtCamera",
          "FaceVelocity": false,
          "Additive": true,
          "Shadows": false,
          "Lighting": false,
          "DepthFeather": 0,
          "SortMode": "Unsorted",
          "Opaque": false,
          "FogStrength": 1,
          "TextureFilter": "Bilinear",
          "MotionBlur": false,
          "LeadingTrail": true,
          "BlurAmount": 0.5,
          "BlurSpacing": 0.5,
          "BlurOpacity": 0.5,
          "Identifier": "818d1c9b-6cd4-5188-a9e6-457a6ffd8a02",
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
                "rangey": "0,0.0500000007",
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
                "rangey": "0,0.0500000007",
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
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
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
                    "c": "0.3765,1,0.7529,1"
                  },
                  {
                    "t": 1,
                    "c": "0.3765,1,0.7529,1"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 1
                  },
                  {
                    "t": 1,
                    "a": 0
                  }
                ]
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "0.3765,1,0.7529,1"
                  },
                  {
                    "t": 1,
                    "c": "0.3765,1,0.7529,1"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 1
                  },
                  {
                    "t": 1,
                    "a": 0
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
          "PointDistance": 0.04,
          "LifeTime": 0.6,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": true,
          "TintFromParticle": true,
          "Identifier": "2eee550d-a1ad-5525-91ff-105407c99282",
          "Name": "Trail",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Streamers Copy Copy",
      "Identifier": "ac59971f-a724-486f-a9b1-377c323b9a09",
      "Enabled": true,
      "MaxParticles": 60,
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
          "__type": "Rinten.SpawnRateModule",
          "Stage": "Spawn",
          "Rate": {
            "UseParameter": true,
            "Value": 10,
            "ParameterName": "Intensity",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Identifier": "72e0814f-3551-5998-a3ea-81115c336c10",
          "Name": "Spawn Rate",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": "Helix",
          "Sample": "ByTime",
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
          "Shape": "Point",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "ce8d06af-b5c9-5e63-be84-a616d5db27d1",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 1.8,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "7921d794-ffc0-58d6-8557-e42096b685cc",
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
                "rangey": "0,0.100000001",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.2,
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
                    "y": 0,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,0.100000001",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.2,
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
                    "y": 0,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              }
            },
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "540e6761-1f2b-58ac-8c31-bd7dc2d10308",
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
                    "c": "0.502,1,0.6902,1"
                  },
                  {
                    "t": 0.6,
                    "c": "0.251,0.8784,1,1"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,1"
                  }
                ],
                "alpha": null
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "0.502,1,0.6902,1"
                  },
                  {
                    "t": 0.6,
                    "c": "0.251,0.8784,1,1"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,1"
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
            "Value": 2,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "3b0d9cd5-47c7-59ed-8751-981b630230a4",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Helix 2 2",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": true,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": [
                {
                  "x": 0,
                  "y": 0,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                },
                {
                  "x": 1,
                  "y": 1,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                }
              ],
              "CurveB": [
                {
                  "x": 0,
                  "y": 0,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                },
                {
                  "x": 1,
                  "y": 1,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                }
              ]
            },
            "ParameterName": "Rise",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Stagger": {
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
          "Speed": {
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
          "Loop": false,
          "Weight": {
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
          "AlignToShape": true,
          "Identifier": "26902e6e-4513-56b9-9ccc-4cec898a6dcf",
          "Name": "Follow Shape",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/glow.sprite",
          "Scale": 1,
          "Alignment": "LookAtCamera",
          "FaceVelocity": false,
          "Additive": true,
          "Shadows": false,
          "Lighting": false,
          "DepthFeather": 0,
          "SortMode": "Unsorted",
          "Opaque": false,
          "FogStrength": 1,
          "TextureFilter": "Bilinear",
          "MotionBlur": false,
          "LeadingTrail": true,
          "BlurAmount": 0.5,
          "BlurSpacing": 0.5,
          "BlurOpacity": 0.5,
          "Identifier": "818d1c9b-6cd4-5188-a9e6-457a6ffd8a02",
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
                "rangey": "0,0.0500000007",
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
                "rangey": "0,0.0500000007",
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
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
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
                    "c": "0.3765,1,0.7529,1"
                  },
                  {
                    "t": 1,
                    "c": "0.3765,1,0.7529,1"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 1
                  },
                  {
                    "t": 1,
                    "a": 0
                  }
                ]
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "0.3765,1,0.7529,1"
                  },
                  {
                    "t": 1,
                    "c": "0.3765,1,0.7529,1"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 1
                  },
                  {
                    "t": 1,
                    "a": 0
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
          "PointDistance": 0.04,
          "LifeTime": 0.6,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": true,
          "TintFromParticle": true,
          "Identifier": "2eee550d-a1ad-5525-91ff-105407c99282",
          "Name": "Trail",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Streamers Copy Copy Copy",
      "Identifier": "1d486e1e-c016-436d-be7f-b18a9816f6ed",
      "Enabled": true,
      "MaxParticles": 60,
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
          "__type": "Rinten.SpawnRateModule",
          "Stage": "Spawn",
          "Rate": {
            "UseParameter": true,
            "Value": 10,
            "ParameterName": "Intensity",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Identifier": "72e0814f-3551-5998-a3ea-81115c336c10",
          "Name": "Spawn Rate",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": "Helix",
          "Sample": "ByTime",
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
          "Shape": "Point",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "ce8d06af-b5c9-5e63-be84-a616d5db27d1",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 1.8,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "7921d794-ffc0-58d6-8557-e42096b685cc",
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
                "rangey": "0,0.100000001",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.2,
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
                    "y": 0,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,0.100000001",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.2,
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
                    "y": 0,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              }
            },
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "540e6761-1f2b-58ac-8c31-bd7dc2d10308",
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
                    "c": "0.502,1,0.6902,1"
                  },
                  {
                    "t": 0.6,
                    "c": "0.251,0.8784,1,1"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,1"
                  }
                ],
                "alpha": null
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "0.502,1,0.6902,1"
                  },
                  {
                    "t": 0.6,
                    "c": "0.251,0.8784,1,1"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,1"
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
            "Value": 2,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "3b0d9cd5-47c7-59ed-8751-981b630230a4",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Helix 2 2 2",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": true,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": [
                {
                  "x": 0,
                  "y": 0,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                },
                {
                  "x": 1,
                  "y": 1,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                }
              ],
              "CurveB": [
                {
                  "x": 0,
                  "y": 0,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                },
                {
                  "x": 1,
                  "y": 1,
                  "in": 0,
                  "out": 0,
                  "mode": "Linear"
                }
              ]
            },
            "ParameterName": "Rise",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Stagger": {
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
          "Speed": {
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
          "Loop": false,
          "Weight": {
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
          "AlignToShape": true,
          "Identifier": "26902e6e-4513-56b9-9ccc-4cec898a6dcf",
          "Name": "Follow Shape",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/glow.sprite",
          "Scale": 1,
          "Alignment": "LookAtCamera",
          "FaceVelocity": false,
          "Additive": true,
          "Shadows": false,
          "Lighting": false,
          "DepthFeather": 0,
          "SortMode": "Unsorted",
          "Opaque": false,
          "FogStrength": 1,
          "TextureFilter": "Bilinear",
          "MotionBlur": false,
          "LeadingTrail": true,
          "BlurAmount": 0.5,
          "BlurSpacing": 0.5,
          "BlurOpacity": 0.5,
          "Identifier": "818d1c9b-6cd4-5188-a9e6-457a6ffd8a02",
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
                "rangey": "0,0.0500000007",
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
                "rangey": "0,0.0500000007",
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
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
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
                    "c": "0.3765,1,0.7529,1"
                  },
                  {
                    "t": 1,
                    "c": "0.3765,1,0.7529,1"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 1
                  },
                  {
                    "t": 1,
                    "a": 0
                  }
                ]
              },
              "GradientB": {
                "blend": "Linear",
                "color": [
                  {
                    "t": 0,
                    "c": "0.3765,1,0.7529,1"
                  },
                  {
                    "t": 1,
                    "c": "0.3765,1,0.7529,1"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 1
                  },
                  {
                    "t": 1,
                    "a": 0
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
          "PointDistance": 0.04,
          "LifeTime": 0.6,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": true,
          "TintFromParticle": true,
          "Identifier": "2eee550d-a1ad-5525-91ff-105407c99282",
          "Name": "Trail",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Motes",
      "Identifier": "cdc53ce9-8c1e-5bf8-80e8-6fc6ae88b841",
      "Enabled": true,
      "MaxParticles": 120,
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
          "__type": "Rinten.SpawnRateModule",
          "Stage": "Spawn",
          "Rate": {
            "UseParameter": true,
            "Value": 40,
            "ParameterName": "Intensity",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Identifier": "cae382b2-3e9b-515a-9fbc-2de225c57a74",
          "Name": "Spawn Rate",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": "Rim",
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
          "Shape": "Point",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "a34615b1-8418-5871-98b8-9d48fee02018",
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
              "Y": 0.5,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1,
            "ScaleParameterName": null,
            "SlotName": null,
            "SlotMode": "Replace",
            "IsBound": false
          },
          "Scatter": {
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
          "LocalSpace": false,
          "InheritEmitterVelocity": false,
          "InheritScale": 1,
          "Drift": {
            "X": 0,
            "Y": 0,
            "Z": 0
          },
          "Identifier": "0aca5bc8-35b1-506b-b627-cb00a1145c3b",
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
              "Constants": "1.20000005,2,0,0"
            },
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "9e659202-84ba-5275-ad20-55ffbfe5f2b4",
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
              "Constants": "0.0149999997,0.0299999993,0,0"
            },
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "b86cbd39-ac4f-5a08-bc3a-d7fcdc2f0b81",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.7529,1,0.8784,1",
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
                  "y": 0,
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
                  "y": 0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                }
              ],
              "CurveB": [
                {
                  "x": 0,
                  "y": 0,
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
                  "y": 0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                }
              ]
            },
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
            "Value": 1.5,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "a02391e9-dbd3-5e61-8527-065959e4333a",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.DragModule",
          "Stage": "Update",
          "Damping": {
            "UseParameter": false,
            "Value": 0.4,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "c3052230-e448-5539-bb6d-3fba3ab9fd36",
          "Name": "Drag",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/dot.sprite",
          "Scale": 1,
          "Alignment": "LookAtCamera",
          "FaceVelocity": false,
          "Additive": true,
          "Shadows": false,
          "Lighting": false,
          "DepthFeather": 0,
          "SortMode": "Unsorted",
          "Opaque": false,
          "FogStrength": 1,
          "TextureFilter": "Bilinear",
          "MotionBlur": false,
          "LeadingTrail": true,
          "BlurAmount": 0.5,
          "BlurSpacing": 0.5,
          "BlurOpacity": 0.5,
          "Identifier": "e32d9d69-2577-55de-ac3f-6df9a47056e3",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Ground Glow",
      "Identifier": "b983147c-4486-5791-8c45-4152fd9fa3c0",
      "Enabled": true,
      "MaxParticles": 1,
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
          "Identifier": "40d263da-5332-5e8a-8324-9371a024526b",
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
          "Shape": "Point",
          "Offset": "0,0.0500000007,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "e227d311-7fcb-56b3-8b80-9d39c78908e5",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 10000,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "7bd0c6ba-3a1f-55e6-bc62-64ddeb67c8fc",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 2.2,
            "ParameterName": "Size",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "InheritEmitterScale": true,
          "Identifier": "649f98ae-c069-5b71-bcb8-ef5429bce6e8",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.3765,1,0.6902,1",
            "ParameterName": null,
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": 0.18,
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
            "Value": 1,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "fbb2e737-df13-56f9-bf57-7736b9061512",
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
          "Scale": 1,
          "Alignment": "LookAtCamera",
          "FaceVelocity": false,
          "Additive": true,
          "Shadows": false,
          "Lighting": false,
          "DepthFeather": 0,
          "SortMode": "Unsorted",
          "Opaque": false,
          "FogStrength": 1,
          "TextureFilter": "Bilinear",
          "MotionBlur": false,
          "LeadingTrail": true,
          "BlurAmount": 0.5,
          "BlurSpacing": 0.5,
          "BlurOpacity": 0.5,
          "Identifier": "d5e56190-353b-5a59-9493-9029015dd3a7",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 6,
  "Looping": true,
  "Shapes": [
    {
      "Name": "Ring",
      "Identifier": "7b840851-5a30-56ab-8d1a-9b86942b2c05",
      "Kind": "Circle",
      "Anchor": null,
      "Offset": "0,0.150000006,0",
      "Rotation": "0,0,0",
      "Radius": 0.9,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": true,
      "LineStart": "0,0,0",
      "LineEnd": "0,1,0",
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Points": [],
      "Closed": false,
      "GridCount": "5,1,5",
      "GridSpacing": "0.300000012,0.300000012,0.300000012",
      "Height": 2,
      "Turns": 3,
      "Count": 8
    },
    {
      "Name": "Helix",
      "Identifier": "cdc310a8-ab45-5222-87c0-5b14cdf0509a",
      "Kind": "Helix",
      "Anchor": null,
      "Offset": "0,0.100000001,0",
      "Rotation": "0,0,0",
      "Radius": 0.55,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": false,
      "LineStart": "0,0,0",
      "LineEnd": "0,1,0",
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Points": [],
      "Closed": false,
      "GridCount": "5,1,5",
      "GridSpacing": "0.300000012,0.300000012,0.300000012",
      "Height": 2.4,
      "Turns": 1.5,
      "Count": 0
    },
    {
      "Name": "Helix 2",
      "Identifier": "10155af4-5ae4-4dfe-9f82-f4b3b7e99881",
      "Kind": "Helix",
      "Anchor": null,
      "Offset": "0,0.100000001,0",
      "Rotation": "0,90,0",
      "Radius": 0.55,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": false,
      "LineStart": "0,0,0",
      "LineEnd": "0,1,0",
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Points": [],
      "Closed": false,
      "GridCount": "5,1,5",
      "GridSpacing": "0.300000012,0.300000012,0.300000012",
      "Height": 2.4,
      "Turns": 1.5,
      "Count": 0
    },
    {
      "Name": "Helix 2 2",
      "Identifier": "3da69884-b7e4-48af-8cbc-7f60896c30b1",
      "Kind": "Helix",
      "Anchor": null,
      "Offset": "0,0.100000001,0",
      "Rotation": "0,180,0",
      "Radius": 0.55,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": false,
      "LineStart": "0,0,0",
      "LineEnd": "0,1,0",
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Points": [],
      "Closed": false,
      "GridCount": "5,1,5",
      "GridSpacing": "0.300000012,0.300000012,0.300000012",
      "Height": 2.4,
      "Turns": 1.5,
      "Count": 0
    },
    {
      "Name": "Helix 2 2 2",
      "Identifier": "6f518089-1a5a-4bd3-80df-e954dd5671d5",
      "Kind": "Helix",
      "Anchor": null,
      "Offset": "0,0.100000001,0",
      "Rotation": "0,270,0",
      "Radius": 0.55,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1,
      "BoxSize": "1,1,1",
      "ConeAngle": 45,
      "OnShell": false,
      "LineStart": "0,0,0",
      "LineEnd": "0,1,0",
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Points": [],
      "Closed": false,
      "GridCount": "5,1,5",
      "GridSpacing": "0.300000012,0.300000012,0.300000012",
      "Height": 2.4,
      "Turns": 1.5,
      "Count": 0
    },
    {
      "Name": "Rim",
      "Identifier": "42d936f6-5d38-5846-82f0-a084872fc318",
      "Kind": "Cone",
      "Anchor": null,
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Radius": 0.4,
      "Model": null,
      "ModelSampling": "Parts",
      "ModelScale": 1,
      "BoxSize": "1,1,1",
      "ConeAngle": 65,
      "OnShell": true,
      "LineStart": "0,0,0",
      "LineEnd": "0,1,0",
      "LineStartAnchor": null,
      "LineEndAnchor": null,
      "Points": [],
      "Closed": false,
      "GridCount": "5,1,5",
      "GridSpacing": "0.300000012,0.300000012,0.300000012",
      "Height": 2,
      "Turns": 3,
      "Count": 0
    }
  ],
  "Slots": [],
  "Anchors": [],
  "FloatParameters": [
    {
      "DefaultValue": 1,
      "Min": -3,
      "Max": 3,
      "Name": "Spin",
      "Identifier": "88565ac8-e6a8-5c18-9984-ca2f7499ee8a"
    },
    {
      "DefaultValue": 1,
      "Min": 0.2,
      "Max": 3,
      "Name": "Rise",
      "Identifier": "a5acf07d-0d89-560e-881c-a95aade8dd42"
    },
    {
      "DefaultValue": 1,
      "Min": 0,
      "Max": 3,
      "Name": "Intensity",
      "Identifier": "ff7f7d2f-2f2e-5b9a-ac9f-61907d602d66"
    },
    {
      "DefaultValue": 1,
      "Min": 0.2,
      "Max": 3,
      "Name": "Size",
      "Identifier": "aa28643f-24dc-5d1d-8f12-1fa1d19f187c"
    }
  ],
  "VectorParameters": [],
  "ColorParameters": [],
  "__references": [],
  "__version": 0
}