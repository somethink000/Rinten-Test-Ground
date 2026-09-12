{
  "Emitters": [
    {
      "Name": "Nucleus",
      "Identifier": "a12ca8a4-a6ec-501a-a71c-dfb7105e609e",
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
          "Identifier": "f6d59346-b80c-5eb5-930b-c7bd5c6b6e7c",
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
          "Identifier": "083a0ad5-61af-5efe-8b60-7390f07ce0de",
          "Name": "Position",
          "Enabled": true,
          "ShapeName": "Path",
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
          "Identifier": "69258958-48f6-5a0d-b444-a884a489284e",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": 0.35,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "64cc3412-707a-5d1c-afa2-7379ea5676fc",
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
          "Identifier": "87d6fadb-0225-5705-9014-d87143b3c7a2",
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
              "X": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-40,40,0,0"
              },
              "Y": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-40,40,0,0"
              },
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
          "Identifier": "fa42efc9-1d00-5c18-816f-d40efe0261e4",
          "Name": "Spin",
          "Enabled": true
        },
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Path",
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
            "Value": 0.014285714285714285,
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
          "Identifier": "052d52fe-b5c0-5ab1-8249-f6ccf28d4637",
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
              "AnchorName": "Comet"
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
          "Identifier": "68c1bbcf-f9ab-591e-9f2e-5f0f28652c17",
          "Name": "Publish Comet",
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
          "Effect": "fx/sol_comet_tail.fx",
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
          "Identifier": "37f3ccb3-747b-58b6-a66c-8e5a4e423d66",
          "Name": "Tail",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/box.mdl",
          "Material": "materials/solar/rock.mat",
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
              "Name": "Emission",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.9,
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
          "Identifier": "1192de9c-bb71-5812-9ed2-318d8e596b8e",
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
                "rangey": "0,1.4",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.19999999999999998,
                    "in": 0,
                    "out": 0,
                    "mode": "Linear"
                  },
                  {
                    "x": 1,
                    "y": 1.0,
                    "in": 0,
                    "out": 0,
                    "mode": "Linear"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,1.4",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.19999999999999998,
                    "in": 0,
                    "out": 0,
                    "mode": "Linear"
                  },
                  {
                    "x": 1,
                    "y": 1.0,
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
                    "c": "0.8784,0.9412,1.0000,0.35"
                  },
                  {
                    "t": 1,
                    "c": "0.8784,0.9412,1.0000,0.35"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.35
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
                    "c": "0.8784,0.9412,1.0000,0.35"
                  },
                  {
                    "t": 1,
                    "c": "0.8784,0.9412,1.0000,0.35"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.35
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
          "MaxPoints": 120,
          "PointDistance": 0.1,
          "LifeTime": 6.0,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": false,
          "TintFromParticle": false,
          "Identifier": "5ba79568-0e5a-5890-9acf-1501db91b693",
          "Name": "Trail",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "0.7529,0.8784,1.0000,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 2,
            "ParameterName": null,
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
            "Value": 1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "UseParticleColor": false,
          "CastShadows": false,
          "Identifier": "4d827b43-e810-5a4c-9aac-1da0ad080276",
          "Name": "Light",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 10,
  "Looping": true,
  "Shapes": [
    {
      "Name": "Path",
      "Identifier": "b03e0fb7-8152-51f2-a52e-e236dd9b2f46",
      "Kind": "Spline",
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
      "Points": [
        "-4.0,0.5,-3.0",
        "10.0,1.5,12.0",
        "34.0,3.0,40.0",
        "60.0,2.0,30.0",
        "52.0,-1.0,-8.0",
        "24.0,-2.0,-30.0",
        "2.0,-0.5,-18.0"
      ],
      "Closed": true,
      "GridCount": "5,1,5",
      "GridSpacing": "0.3,0.3,0.3",
      "Height": 2.0,
      "Turns": 3.0,
      "Count": 0
    }
  ],
  "Slots": [],
  "Anchors": [
    {
      "Name": "Comet",
      "Identifier": "d1574af8-3572-5421-90fe-d4a7b9fe49bc",
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1"
    }
  ],
  "FloatParameters": [
    {
      "Name": "Speed",
      "DefaultValue": 1,
      "Min": 0.1,
      "Max": 5,
      "Identifier": "c5652ff3-2ee3-566a-8605-b1bee9390b2f"
    },
    {
      "Name": "Tail",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 3,
      "Identifier": "cb5dbcaa-174a-5fee-9ad5-06600ef50ff7"
    }
  ],
  "VectorParameters": [],
  "ColorParameters": [],
  "__references": [],
  "__version": 0
}