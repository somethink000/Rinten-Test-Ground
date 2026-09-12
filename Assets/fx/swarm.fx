{
  "Emitters": [
    {
      "Name": "Sun",
      "Identifier": "32022839-25b5-5ac0-bd20-2844025dc062",
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
          "Identifier": "cbc7c493-e667-5649-a1cf-c593c384b030",
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
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "f680e93d-6bf8-5714-9d26-3733fd11e5ee",
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
          "Identifier": "3c55e9da-ae31-555a-8ba0-182a15f75181",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.5,
            "ParameterName": "Size",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "InheritEmitterScale": true,
          "Identifier": "05d793af-0872-5ca0-a0a8-6e17bf8064bb",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "1,1,1,1",
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
          "Identifier": "3a2ddff0-a394-5c5c-9039-70f6acb01a80",
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
              "Y": 20,
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1,
            "ScaleParameterName": null,
            "SlotName": null,
            "SlotMode": "Replace",
            "IsBound": false
          },
          "Identifier": "62eeec5c-ff63-56c4-b2d8-e17625837d3e",
          "Name": "Spin",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/sphere.mdl",
          "Material": "materials/fx/stylized_ember.mat",
          "Scale": {
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
          "RotateWithObject": false,
          "CastShadows": false,
          "Morphs": [],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
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
                "Value": 0.1,
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
                "Value": 2.5,
                "ParameterName": "Glow",
                "SlotName": null,
                "SlotChannel": "X",
                "SlotMode": "Replace",
                "Mode": "Multiply",
                "Multiplier": 1,
                "IsBound": true
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
          "PartFromParticle": false,
          "Identifier": "8eadf57b-31f5-5f5e-aae0-68a425850eef",
          "Name": "Mesh",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Corona",
      "Identifier": "d214178d-d49c-520d-98f9-d8328f207c8e",
      "Enabled": true,
      "MaxParticles": 8,
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
            "UseParameter": false,
            "Value": 3,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "d1eb8bb1-6893-50e4-aa4f-c146908e549e",
          "Name": "Spawn Rate",
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
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "dbd4c2c5-cac1-52fb-99f3-ac173aac7dd0",
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
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "42006e2b-9f84-5117-aaae-f29bb084dc06",
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
                "rangey": "0,1.5",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.6,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 0.5,
                    "y": 0.8666667,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.6,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              },
              "CurveB": {
                "rangey": "0,1.5",
                "frames": [
                  {
                    "x": 0,
                    "y": 0.6,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 0.5,
                    "y": 0.8666667,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  },
                  {
                    "x": 1,
                    "y": 0.6,
                    "in": 0,
                    "out": 0,
                    "mode": "Flat"
                  }
                ]
              }
            },
            "ParameterName": "Size",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "InheritEmitterScale": true,
          "Identifier": "3b5cb12b-4abd-5241-963d-7db22cb3acf2",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "1,0.8471,0.6275,1",
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
                  "x": 0.5,
                  "y": 0.35,
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
                  "x": 0.5,
                  "y": 0.35,
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
            "Value": 1.2,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "91e47b4b-91aa-510a-87a2-02100448de0d",
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
          "Identifier": "1948a745-c28d-5c15-a0b4-fb4d62335333",
          "Name": "Sprite",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "1,0.8471,0.6275,1",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": true,
            "Value": 6,
            "ParameterName": "Glow",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Radius": {
            "UseParameter": false,
            "Value": 5,
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
            "Value": 1,
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
            "Value": 0.5,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "UseParticleColor": false,
          "CastShadows": false,
          "Identifier": "63812903-b69d-5871-b2c8-1cd3ad52cb78",
          "Name": "Light",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Orbit 1",
      "Identifier": "7bb49126-df16-529c-b162-6b4d8ae416f7",
      "Enabled": true,
      "MaxParticles": 80,
      "Places": 80,
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
            "Value": 80,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "0ff72ccf-37a8-559e-8531-1c16c6111884",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": "Orbit 1",
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
          "Identifier": "e7744ea0-f815-5d49-b67d-12b113a2266a",
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
          "Identifier": "3b501cc5-25b3-58d0-816b-9048f59cd50d",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.012,
            "ParameterName": "Size",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "InheritEmitterScale": true,
          "Identifier": "5ae7ded8-8d40-5781-aad3-9247d4b2eb4e",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.7529,0.8157,0.8784,1",
            "ParameterName": null,
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": 0.22,
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
          "Identifier": "454db8c3-e192-5f7f-be44-aa44f5928a25",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Orbit 1",
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
          "Identifier": "c85b01a8-3a6b-5287-91c3-dc4d9aeb79c0",
          "Name": "Follow Shape",
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
          "Identifier": "12ff5974-168d-57da-b032-d717715aad1a",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Orbit 2",
      "Identifier": "1b13fee3-c6ed-500b-99e7-f2a5c016fc9f",
      "Enabled": true,
      "MaxParticles": 120,
      "Places": 120,
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
            "Value": 120,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "aafbd51c-b032-5dc6-bbd4-5b9fc1ff0986",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": "Orbit 2",
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
          "Identifier": "1a975669-bfb1-5bda-b542-20f9ac18d8d8",
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
          "Identifier": "920cdb95-f3d0-52d6-8d26-ad20bff20149",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.012,
            "ParameterName": "Size",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "InheritEmitterScale": true,
          "Identifier": "215e5371-1e60-54d8-867b-d3ea08c652a6",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.7529,0.8157,0.8784,1",
            "ParameterName": null,
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": 0.22,
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
          "Identifier": "9f111560-7bea-5878-a886-81d39edf7f05",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Orbit 2",
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
          "Identifier": "d47b32fc-d244-5bea-9947-eb7d676b8919",
          "Name": "Follow Shape",
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
          "Identifier": "bfbe2071-a7bb-517a-b77b-871d19fd4023",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Orbit 3",
      "Identifier": "da7a5046-db34-54a9-ab5c-a34f9d495567",
      "Enabled": true,
      "MaxParticles": 160,
      "Places": 160,
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
            "Value": 160,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "7ac95f37-90f3-5c8b-b1f9-d62dce0e083e",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": "Orbit 3",
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
          "Identifier": "ff39b0b8-a061-59a5-a34e-ff6532c366c1",
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
          "Identifier": "c4007598-13bb-5f28-858f-83e224541e56",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.012,
            "ParameterName": "Size",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "InheritEmitterScale": true,
          "Identifier": "8333eda7-9310-5ed5-b793-50f92b62e3b9",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.7529,0.8157,0.8784,1",
            "ParameterName": null,
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": 0.22,
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
          "Identifier": "5f58cf58-a002-5b26-8f79-d236b8cb0681",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Orbit 3",
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
          "Identifier": "eba2f777-aa28-5c1b-88bb-1dc94b34374f",
          "Name": "Follow Shape",
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
          "Identifier": "b1379a4b-d637-5fb1-b6b9-bff2a48ec4ef",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Inner Planet",
      "Identifier": "a6c7d7f3-471a-5ef0-99f7-91766ed5be9c",
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
          "Identifier": "fe0c43b7-44db-5b61-aded-b91bb61f3023",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": "Orbit 1",
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
          "Identifier": "7a34d393-ad83-5ae4-9ac5-af046efca6c4",
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
          "Identifier": "c4475e79-9b87-5767-a9b6-fecfa0ebca75",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.16,
            "ParameterName": "Size",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "InheritEmitterScale": true,
          "Identifier": "cf85d1f1-4c3b-5b17-91a5-4cef071dd8e2",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": "1,1,1,1",
            "ParameterName": "Inner",
            "IsBound": true
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
          "Identifier": "57eb0925-3019-55a6-840c-e1c207f6baf3",
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
              "Y": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "30,60,0,0"
              },
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1,
            "ScaleParameterName": null,
            "SlotName": null,
            "SlotMode": "Replace",
            "IsBound": false
          },
          "Identifier": "ce9924c2-b98d-598d-85e0-01d13f86089a",
          "Name": "Spin",
          "Enabled": true
        },
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Orbit 1",
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
            "Value": 0.2,
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
          "Identifier": "d8078a63-a985-5973-b833-de4d26b50cb4",
          "Name": "Follow Shape",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/sphere.mdl",
          "Material": "materials/fx/stylized_white.mat",
          "Scale": {
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
          "RotateWithObject": false,
          "CastShadows": true,
          "Morphs": [],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
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
                "Value": 0.05,
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
                "UseParameter": false,
                "Value": 0.9,
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
                "UseParameter": false,
                "Value": 0.6,
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
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            }
          ],
          "ParticleAttributes": true,
          "PartFromParticle": false,
          "Identifier": "da6ce7d1-fdba-5c89-ab5c-f94fc2b961d0",
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
                "rangey": "0,0.5",
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
                "rangey": "0,0.5",
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
                    "c": "1,1,1,0.35"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,0.35"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.35
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
                    "c": "1,1,1,0.35"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,0.35"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.35
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
          "MaxPoints": 60,
          "PointDistance": 0.04,
          "LifeTime": 0.9,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": true,
          "TintFromParticle": true,
          "Identifier": "eaf57965-d067-5051-bc1f-f378b7ee84c1",
          "Name": "Trail",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "1,1,1,1",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
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
          "Radius": {
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
            "Value": 1,
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
          "Identifier": "2157fa59-25aa-5fca-b406-1f654451f4a8",
          "Name": "Light",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Middle Planet",
      "Identifier": "30a34f15-fcda-5ec3-8d7b-e156bfa20c0e",
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
          "Identifier": "40a033c9-6392-5e3d-8236-c2d16ffdc4c5",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": "Orbit 2",
          "Sample": "ByTime",
          "Along": {
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
          "Identifier": "65cc4974-c93d-5351-a832-c120faa75411",
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
          "Identifier": "18a1c1be-045d-5427-a7f3-63f9ce1e473d",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.28,
            "ParameterName": "Size",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "InheritEmitterScale": true,
          "Identifier": "6d46bcd7-a5e2-5868-8bf3-5644b8f7fae2",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": "1,1,1,1",
            "ParameterName": "Middle",
            "IsBound": true
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
          "Identifier": "6a5508ba-3845-5fe9-897c-56ad25be3149",
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
              "Y": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "30,60,0,0"
              },
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1,
            "ScaleParameterName": null,
            "SlotName": null,
            "SlotMode": "Replace",
            "IsBound": false
          },
          "Identifier": "2bed4592-d28a-5a24-9159-333f5ad172f5",
          "Name": "Spin",
          "Enabled": true
        },
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Orbit 2",
          "Sample": "ByTime",
          "Along": {
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
            "Value": -0.11,
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
          "Identifier": "1d7351cf-912f-5fe7-8ac6-573dc6ffe1cf",
          "Name": "Follow Shape",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/sphere.mdl",
          "Material": "materials/fx/stylized_white.mat",
          "Scale": {
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
          "RotateWithObject": false,
          "CastShadows": true,
          "Morphs": [],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
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
                "Value": 0.05,
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
                "UseParameter": false,
                "Value": 0.9,
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
                "UseParameter": false,
                "Value": 0.6,
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
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            }
          ],
          "ParticleAttributes": true,
          "PartFromParticle": false,
          "Identifier": "339435fd-fad7-5494-815e-785766870829",
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
                "rangey": "0,0.5",
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
                "rangey": "0,0.5",
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
                    "c": "1,1,1,0.35"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,0.35"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.35
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
                    "c": "1,1,1,0.35"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,0.35"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.35
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
          "MaxPoints": 60,
          "PointDistance": 0.04,
          "LifeTime": 0.9,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": true,
          "TintFromParticle": true,
          "Identifier": "661ab2b0-798d-596e-9bd4-4a23abfd6b01",
          "Name": "Trail",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "1,1,1,1",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
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
          "Radius": {
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
            "Value": 1,
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
          "Identifier": "9152759d-d4b0-542b-ad0c-314455159493",
          "Name": "Light",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Outer Planet",
      "Identifier": "00e3ae7b-3309-599e-8e53-a5b0f833f862",
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
          "Identifier": "7637115b-afdb-5889-8824-847f7dcbb980",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "ShapeName": "Orbit 3",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": false,
            "Value": 0.75,
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
          "Identifier": "80cc823c-b4d2-57a6-bdf6-1142cf41562f",
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
          "Identifier": "955c089c-8036-5f4e-9963-693e25f4723e",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.22,
            "ParameterName": "Size",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "InheritEmitterScale": true,
          "Identifier": "7f0fa149-d1a5-58b0-942e-c29fbf776c69",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": "1,1,1,1",
            "ParameterName": "Outer",
            "IsBound": true
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
          "Identifier": "a9ddd8a8-e23e-5012-b929-ad3b4a65b801",
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
              "Y": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "30,60,0,0"
              },
              "Z": 0
            },
            "ParameterName": null,
            "Multiplier": 1,
            "ScaleParameterName": null,
            "SlotName": null,
            "SlotMode": "Replace",
            "IsBound": false
          },
          "Identifier": "388a3fc9-b3ba-5ca7-a37b-9cfda5098223",
          "Name": "Spin",
          "Enabled": true
        },
        {
          "__type": "Rinten.FollowShapeModule",
          "Stage": "Update",
          "ShapeName": "Orbit 3",
          "Sample": "ByTime",
          "Along": {
            "UseParameter": false,
            "Value": 0.75,
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
            "Value": 0.07,
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
          "Identifier": "e9664cd6-3237-5271-9d20-d0e01927b813",
          "Name": "Follow Shape",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/dev/sphere.mdl",
          "Material": "materials/fx/stylized_white.mat",
          "Scale": {
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
          "RotateWithObject": false,
          "CastShadows": true,
          "Morphs": [],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
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
                "Value": 0.05,
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
                "UseParameter": false,
                "Value": 0.9,
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
                "UseParameter": false,
                "Value": 0.6,
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
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            }
          ],
          "ParticleAttributes": true,
          "PartFromParticle": false,
          "Identifier": "cee87746-06f3-55c5-b73f-967989bc9c75",
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
                "rangey": "0,0.5",
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
                "rangey": "0,0.5",
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
                    "c": "1,1,1,0.35"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,0.35"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.35
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
                    "c": "1,1,1,0.35"
                  },
                  {
                    "t": 1,
                    "c": "1,1,1,0.35"
                  }
                ],
                "alpha": [
                  {
                    "t": 0,
                    "a": 0.35
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
          "MaxPoints": 60,
          "PointDistance": 0.04,
          "LifeTime": 0.9,
          "Opaque": false,
          "BlendMode": "Normal",
          "ScaleFromParticle": true,
          "TintFromParticle": true,
          "Identifier": "9f02bf9b-8e5c-5895-b04b-f772ac523fca",
          "Name": "Trail",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "1,1,1,1",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
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
          "Radius": {
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
            "Value": 1,
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
          "Identifier": "de9fb9c3-4329-59ff-a829-283a037b288f",
          "Name": "Light",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Dust",
      "Identifier": "e4fdc1ed-f59b-5505-9891-2e4696b05e0a",
      "Enabled": true,
      "MaxParticles": 150,
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
            "Value": 25,
            "ParameterName": "Count",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Identifier": "f20f23a3-b88f-540f-ace1-dcf6892f0f3f",
          "Name": "Spawn Rate",
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
          "Shape": "Circle",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 2.6,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "958d77e8-bcc9-55c3-8981-11cb42c9e7b8",
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
              "Constants": "3,5,0,0"
            },
            "ParameterName": "Lifetime",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Identifier": "87fa5d64-1b7c-59ff-87b1-fb427145ae85",
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
              "Constants": "0.0120000001,0.0250000004,0,0"
            },
            "ParameterName": "Size",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "InheritEmitterScale": true,
          "Identifier": "8fca3d7c-bcc0-554a-9b12-854c9487482f",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "0.8784,0.9098,1,1",
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
                  "x": 0.3,
                  "y": 0.5,
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
                  "x": 0.3,
                  "y": 0.5,
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
          "Identifier": "577aa8f1-8245-52a9-ab7b-b99163069b1b",
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
            "Multiplier": 1,
            "ScaleParameterName": null,
            "SlotName": null,
            "SlotMode": "Replace",
            "IsBound": false
          },
          "Speed": {
            "UseParameter": true,
            "Value": 15,
            "ParameterName": "Spin",
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": true
          },
          "Identifier": "8de408d3-9725-5056-b74b-aee8658ca8d8",
          "Name": "Orbit",
          "Enabled": true
        },
        {
          "__type": "Rinten.CurlNoiseModule",
          "Stage": "Update",
          "Strength": {
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
          "Scale": {
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
          "TimeScale": {
            "UseParameter": false,
            "Value": 0.5,
            "ParameterName": null,
            "SlotName": null,
            "SlotChannel": "X",
            "SlotMode": "Replace",
            "Mode": "Multiply",
            "Multiplier": 1,
            "IsBound": false
          },
          "Offset": "0,0,0",
          "Identifier": "127ebaed-4db8-5826-9be8-a249feeec729",
          "Name": "Curl Noise",
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
          "Identifier": "b34cbf01-aec7-52f5-999b-d1d8599d4666",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 8,
  "Looping": true,
  "Shapes": [
    {
      "Name": "Orbit 1",
      "Identifier": "f0c60bcf-2424-5513-813c-611f531f1126",
      "Kind": "Circle",
      "Anchor": null,
      "Offset": "0,0,0",
      "Rotation": "0,0,6",
      "Radius": 1,
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
      "Count": 0
    },
    {
      "Name": "Orbit 2",
      "Identifier": "6ad2e174-6d17-5849-83bf-9fc0ada96cd1",
      "Kind": "Circle",
      "Anchor": null,
      "Offset": "0,0,0",
      "Rotation": "0,0,-4",
      "Radius": 1.7,
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
      "Count": 0
    },
    {
      "Name": "Orbit 3",
      "Identifier": "506ead3b-7a9e-539f-b32f-f9a806c4bfea",
      "Kind": "Circle",
      "Anchor": null,
      "Offset": "0,0,0",
      "Rotation": "0,0,3",
      "Radius": 2.5,
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
      "Min": 0,
      "Max": 3,
      "Name": "Count",
      "Identifier": "ea3b1a53-79cb-5e55-a1cb-2f920be33ac8"
    },
    {
      "DefaultValue": 1,
      "Min": 0.2,
      "Max": 3,
      "Name": "Size",
      "Identifier": "aa28643f-24dc-5d1d-8f12-1fa1d19f187c"
    },
    {
      "DefaultValue": 1,
      "Min": 0.2,
      "Max": 3,
      "Name": "Lifetime",
      "Identifier": "217a743c-8b19-5549-aa37-f2d90240fd19"
    },
    {
      "DefaultValue": 1,
      "Min": 0,
      "Max": 3,
      "Name": "Glow",
      "Identifier": "6e941755-ba13-5f6b-b668-a3913c5a96a2"
    }
  ],
  "VectorParameters": [],
  "ColorParameters": [
    {
      "DefaultValue": "0.3765,0.8157,1,1",
      "Name": "Inner",
      "Identifier": "756a58fb-731a-5912-bb82-bcaefcf0a820"
    },
    {
      "DefaultValue": "1,0.6902,0.3765,1",
      "Name": "Middle",
      "Identifier": "66fd5807-f243-57ae-9e19-9e31624fc1d0"
    },
    {
      "DefaultValue": "0.7529,0.502,1,1",
      "Name": "Outer",
      "Identifier": "9b2f2e52-793c-5ecc-ac8d-771f8a76a310"
    }
  ],
  "__references": [],
  "__version": 0
}