{
  "Emitters": [
    {
      "Name": "Body",
      "Identifier": "3200b95c-9920-5b5a-bd80-7fa2449a481b",
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
          "Identifier": "a6700376-add3-50ff-89e8-c068a10cfb0c",
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
          "Identifier": "df56bd5d-e6b8-5dae-87e2-a09f273325a0",
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
          "Identifier": "d1cf2f7f-3212-54f2-8dd5-d98abdad9500",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": 0.38,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "ea2d93ac-9b2d-5dc5-8c90-ebf5c3e996fd",
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
          "Identifier": "4bd6bd03-87b0-5807-8745-f2965ea754a4",
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
          "Identifier": "af7c9b45-3b7b-57df-aaf3-b96fb5904752",
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
          "Identifier": "da7c4dbf-488d-540f-b7e6-d5a1bafe0402",
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
          "Identifier": "69b8f5b6-9f27-590a-95e7-4a67c1bd6ce9",
          "Name": "Publish Planet",
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
            }
          ],
          "ParticleAttributes": true,
          "Identifier": "31d34ada-8c91-52dc-ab29-22a881397741",
          "Name": "Mesh",
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