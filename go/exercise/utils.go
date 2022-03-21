package main

import (
	"github.com/tencent-connect/botgo/dto"
)

//NewArk 创建Ark，用来简化ark创建
func NewArk(id int, kv ...*dto.ArkKV) *dto.Ark {
	return &dto.Ark{
		TemplateID: id,
		KV:         kv,
	}
}

//NewArkKV 创建ArkKV，表示key-value
func NewArkKV(key string, value string) *dto.ArkKV {
	return &dto.ArkKV{
		Key:   key,
		Value: value,
	}
}

//NewArkKObj 创建ArkKV，表示key-obj
func NewArkKObj(key string, objKv ...*dto.ArkObjKV) *dto.ArkKV {
	return &dto.ArkKV{
		Key: key,
		Obj: NewArkObj(objKv),
	}
}

//NewArkObj 创建ArkObj的数组
func NewArkObj(objKv []*dto.ArkObjKV) []*dto.ArkObj {
	array := make([]*dto.ArkObj, len(objKv))
	for i := 0; i < len(array); i++ {
		array[i] = &dto.ArkObj{
			ObjKV: []*dto.ArkObjKV{
				objKv[i],
			},
		}
	}
	return array
}

//NewArkObjKV 创建ArkObjKV
func NewArkObjKV(key string, value string) *dto.ArkObjKV {
	return &dto.ArkObjKV{
		Key:   key,
		Value: value,
	}
}

//NewEmbed 创建Embed，用来简化Embed的创建
func NewEmbed(title string, desc string, thumbnail *dto.MessageEmbedThumbnail, fields ...*dto.EmbedField) *dto.Embed {
	return &dto.Embed{
		Title:       title,
		Description: desc,
		Thumbnail:   *thumbnail,
		Fields:      fields,
	}
}

//NewField 创建EmbedField
func NewField(name string) *dto.EmbedField {
	return &dto.EmbedField{Name: name}
}

//NewMessageEmbedThumbnail 创建MessageEmbedThumbnail
func NewMessageEmbedThumbnail(url string) *dto.MessageEmbedThumbnail {
	return &dto.MessageEmbedThumbnail{
		URL: url,
	}
}
