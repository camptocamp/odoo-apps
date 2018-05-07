-- update xmlid for entity_type "Dealer"
-- reuse old entity_type and point new xmlid to it
UPDATE ir_model_data SET res_id = (SELECT res_id FROM ir_model_data WHERE module = '__setup__' AND name = 'res_partner_entity_dealer') WHERE module = 'sf_partner_entity_type' AND name = 'entity_dealer';
-- delete new entity not anymore related to an xmlid
DELETE FROM res_partner_entity_type WHERE name = 'Dealer' AND id != (SELECT res_id FROM ir_model_data WHERE module = 'sf_partner_entity_type' AND name = 'entity_dealer');
