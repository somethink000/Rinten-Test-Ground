{
  "Emitters": [
    {
      "Name": "Shell",
      "Identifier": "e85510a1-49eb-5aef-8e18-ef97b7ba8541",
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
          "Identifier": "44e60248-0dc5-558c-b1bd-edae3480199c",
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
          "Identifier": "dc27128d-02b5-5b88-bb8f-d16226f82961",
          "Name": "Position",
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
          "Identifier": "bf09754e-783a-58e6-8a68-7f0b08c60f27",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 1.0,
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "a3977160-ddc5-5090-968f-77de2c65da37",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": "1,1,1,1",
            "ParameterName": "Tint",
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
          "Identifier": "7164540a-24b1-50ae-85aa-3751cb554c8e",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/shield.mdl",
          "Material": "materials/fx/stylized_shield.mat",
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "RotateWithObject": true,
          "CastShadows": false,
          "PartFromParticle": false,
          "Morphs": [
            {
              "Enabled": true,
              "Name": "Breathe",
              "Weight": {
                "UseParameter": true,
                "Value": {
                  "Type": "Curve",
                  "Evaluation": "Life",
                  "CurveA": [
                    {
                      "x": 0.0,
                      "y": 0.0,
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
                      "x": 1.0,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ],
                  "CurveB": [
                    {
                      "x": 0.0,
                      "y": 0.0,
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
                      "x": 1.0,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ]
                },
                "ParameterName": "Breathe",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              }
            },
            {
              "Enabled": true,
              "Name": "Spike",
              "Weight": {
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
                      "x": 0.1,
                      "y": 0.8,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.4,
                      "y": 0.1,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.7,
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
                      "x": 0.1,
                      "y": 0.8,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.4,
                      "y": 0.1,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.7,
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
                "ParameterName": "Spikes",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              }
            }
          ],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
                "UseParameter": true,
                "Value": 0.35,
                "ParameterName": "Holes",
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
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Edge",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.12,
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
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Emission",
              "Width": 1,
              "Value": {
                "UseParameter": true,
                "Value": 0.9,
                "ParameterName": "Intensity",
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
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Scroll",
              "Width": 1,
              "Value": {
                "UseParameter": true,
                "Value": 0.6,
                "ParameterName": "Speed",
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
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Fresnel",
              "Width": 1,
              "Value": {
                "UseParameter": true,
                "Value": 2.0,
                "ParameterName": "Rim",
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
              "Min": 0,
              "Max": 1
            }
          ],
          "ParticleAttributes": true,
          "Identifier": "3d2110c2-fd3c-58ed-9080-1bb1614bb222",
          "Name": "Mesh",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "0.3765,0.7529,1.0000,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": true,
            "Value": 6,
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
          "Identifier": "09cc06fd-0cf0-5b2d-9550-7ee0d6bd6d19",
          "Name": "Light",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Motes",
      "Identifier": "e18d51c5-a5f8-5d5f-9c40-1bdadfb93a3e",
      "Enabled": true,
      "MaxParticles": 100,
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
            "ParameterName": "Motes",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "1b451d8b-2937-5bc1-a5ba-4176fcb079b7",
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
          "Radius": 0.8,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": true,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "7af8d7a9-ee2e-5973-a680-ac2a3f63c942",
          "Name": "Position",
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
          "Identifier": "65e4b433-f67a-5cd9-91fa-deb35b95d5e2",
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
              "Constants": "0.02,0.04,0,0"
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "13690b88-5c01-558d-ac1a-be9b8493b40d",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.6275,0.8784,1.0000,1.0",
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
                  "x": 0.3,
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
            "UseParameter": false,
            "Value": 1.3,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "b520e4a4-185b-553f-9d2f-4f09dd8ff024",
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
            "Value": 60,
            "ParameterName": "Speed",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "a98ce7d6-d98a-52d3-a164-9269220f43d9",
          "Name": "Orbit",
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
          "Identifier": "dceaa5c9-af06-583b-9582-0f3372e7aa02",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 3.0,
  "Looping": true,
  "Shapes": [],
  "Slots": [],
  "Anchors": [],
  "FloatParameters": [
    {
      "Name": "Intensity",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "ff7f7d2f-2f2e-5b9a-ac9f-61907d602d66"
    },
    {
      "Name": "Breathe",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 2,
      "Identifier": "498b0f1d-a2ca-5c60-89d9-d04c3f596c30"
    },
    {
      "Name": "Spikes",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 2,
      "Identifier": "5c17785a-e497-5029-9b14-ed0135faa62b"
    },
    {
      "Name": "Holes",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 2,
      "Identifier": "bdbda74b-b02d-5577-bcd3-e5e0b74c1d6b"
    },
    {
      "Name": "Rim",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 2,
      "Identifier": "dfcedbe7-e69a-5703-a27b-230e346471cb"
    },
    {
      "Name": "Speed",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "c5652ff3-2ee3-566a-8605-b1bee9390b2f"
    },
    {
      "Name": "Size",
      "DefaultValue": 1,
      "Min": 0.2,
      "Max": 3,
      "Identifier": "aa28643f-24dc-5d1d-8f12-1fa1d19f187c"
    },
    {
      "Name": "Motes",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "df5d6a1f-214f-5eed-b627-33c97ad61b7a"
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
      "Name": "Tint",
      "DefaultValue": "1.0000,1.0000,1.0000,1.0",
      "Identifier": "a1fadc9b-8b11-5fbe-b23f-ac734be678a7"
    }
  ],
  "__references": [],
  "__version": 0
}